import os
import tempfile
from typing import Any
from urllib.parse import urlparse

import boto3
import PyPDF2
from botocore.exceptions import ClientError, NoCredentialsError
from docx import Document

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.config import settings
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class DocumentSummarizerAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id or settings.claude_3_5_sonnet_model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.DOCUMENT_SUMMARIZER)

        # Initialize S3 client using existing settings
        self.s3_client = boto3.client("s3", region_name=settings.aws_region)
        self.temp_files = []  # Track temporary files for cleanup

    def execute(self, context: dict[str, Any]):
        """
        Process uploaded files and create summaries.
        """
        if not self.prompt_service:
            raise ValueError("PromptService is not available for DocumentSummarizerAgent")

        uploaded_files = context.get("uploaded_files", [])
        if not uploaded_files:
            logger.info("No uploaded files to process. Skipping document summarization.")
            return

        logger.info(f"Processing {len(uploaded_files)} uploaded files...")

        document_summaries = []
        for file_url in uploaded_files:
            try:
                # Download file from S3 if it's an S3 URL, otherwise use local path
                local_file_path = self._download_file_if_s3(file_url)

                content = self._extract_content_from_file(local_file_path)
                if content:
                    summary = self._summarize_content(content, file_url)
                    document_summaries.append(
                        {
                            "file_name": self._extract_filename_from_url(file_url),
                            "content": content[:1000] + "..." if len(content) > 1000 else content,  # First 1000 chars
                            "summary": summary,
                        }
                    )
                    logger.info(f"Successfully processed: {self._extract_filename_from_url(file_url)}")
                else:
                    logger.warning(f"Could not extract content from: {self._extract_filename_from_url(file_url)}")
            except Exception as e:
                logger.error(f"Error processing file {file_url}: {str(e)}")
                document_summaries.append(
                    {
                        "file_name": self._extract_filename_from_url(file_url),
                        "content": "",
                        "summary": f"Error processing file: {str(e)}",
                    }
                )

        # Add document summaries to context for the next agent
        context["document_summaries"] = document_summaries

        # Create a consolidated summary for the conversation history
        if document_summaries:
            consolidated_summary = self._create_consolidated_summary(document_summaries)
            existing_history = context.get("conversation_history", [])
            if existing_history:
                # Append to the initial prompt
                updated_initial_prompt = f"{existing_history[0]}\n\nDocument Analysis:\n{consolidated_summary}"
                context["conversation_history"][0] = updated_initial_prompt
            else:
                context["conversation_history"] = [f"Document Analysis:\n{consolidated_summary}"]

            logger.info("Document summaries added to conversation context.")

        # Clean up temporary files
        self._cleanup_temp_files()

    def _download_file_if_s3(self, file_url: str) -> str:
        """
        Download file from S3 if it's an S3 URL, otherwise return the original path.
        """
        if self._is_s3_url(file_url):
            return self._download_from_s3(file_url)
        else:
            return file_url  # Assume it's a local file path

    def _is_s3_url(self, url: str) -> bool:
        """
        Check if the URL is an S3 URL.
        """
        parsed = urlparse(url)
        return parsed.scheme == "s3" or "s3" in parsed.netloc or url.startswith("s3://")

    def _extract_filename_from_url(self, url: str) -> str:
        """
        Extract filename from URL or file path.
        """
        if self._is_s3_url(url):
            # For S3 URLs like s3://bucket/path/file.pdf
            parsed = urlparse(url)
            return os.path.basename(parsed.path)
        else:
            return os.path.basename(url)

    def _download_from_s3(self, s3_url: str) -> str:
        """
        Download file from S3 and return path to temporary local file.
        """
        try:
            # Parse S3 URL (supports both s3://bucket/key and https://bucket.s3.region.amazonaws.com/key formats)
            parsed = urlparse(s3_url)

            if parsed.scheme == "s3":
                bucket = parsed.netloc
                key = parsed.path.lstrip("/")
            else:
                # Handle https://bucket.s3.region.amazonaws.com/key format
                bucket = parsed.netloc.split(".")[0]
                key = parsed.path.lstrip("/")

            # Create temporary file
            file_extension = os.path.splitext(key)[1]
            temp_file = tempfile.NamedTemporaryFile(suffix=file_extension, delete=False)
            temp_file.close()

            # Track for cleanup
            self.temp_files.append(temp_file.name)

            # Download from S3
            logger.info(f"Downloading from S3: s3://{bucket}/{key}")
            self.s3_client.download_file(bucket, key, temp_file.name)

            return temp_file.name

        except (ClientError, NoCredentialsError) as e:
            logger.error(f"S3 error downloading {s3_url}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error downloading file from S3 {s3_url}: {str(e)}")
            raise

    def _cleanup_temp_files(self):
        """
        Clean up temporary files downloaded from S3.
        """
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    logger.debug(f"Cleaned up temporary file: {temp_file}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file {temp_file}: {str(e)}")

        self.temp_files.clear()

    def _extract_content_from_file(self, file_path: str) -> str:
        """
        Extract text content from PDF or Word documents.
        """
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == ".pdf":
            return self._extract_pdf_content(file_path)
        elif file_extension in [".doc", ".docx"]:
            return self._extract_docx_content(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_extension}")
            return ""

    def _extract_pdf_content(self, file_path: str) -> str:
        """
        Extract text content from PDF files.
        """
        text_content = ""
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text() + "\n"
        except Exception as e:
            logger.error(f"Error reading PDF file {file_path}: {str(e)}")
            raise

        return text_content.strip()

    def _extract_docx_content(self, file_path: str) -> str:
        """
        Extract text content from Word documents.
        """
        text_content = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"
        except Exception as e:
            logger.error(f"Error reading DOCX file {file_path}: {str(e)}")
            raise

        return text_content.strip()

    def _summarize_content(self, content: str, file_url: str) -> str:
        """
        Create a summary of the document content using the AI agent.
        """
        file_name = self._extract_filename_from_url(file_url)

        if not self.prompt_service:
            return f"Summary of {file_name}: {content[:200]}..."

        try:
            prompt = self.prompt_service.format_user_prompt(
                AgentType.DOCUMENT_SUMMARIZER, "summarize", content=content, file_name=file_name
            )
            summary = self._agent(prompt)
            return str(summary)
        except Exception as e:
            logger.error(f"Error summarizing content for {file_url}: {str(e)}")
            return f"Could not generate summary: {str(e)}"

    def _create_consolidated_summary(self, document_summaries: list[dict]) -> str:
        """
        Create a consolidated summary of all processed documents.
        """
        if not document_summaries:
            return ""

        if not self.prompt_service:
            # Fallback to simple concatenation
            return "\n\n".join([f"Document: {doc['file_name']} - {doc['summary']}" for doc in document_summaries])

        try:
            summaries_text = "\n\n".join(
                [f"File: {doc['file_name']}\nSummary: {doc['summary']}" for doc in document_summaries]
            )

            prompt = self.prompt_service.format_user_prompt(
                AgentType.DOCUMENT_SUMMARIZER, "consolidate", summaries=summaries_text
            )
            consolidated = self._agent(prompt)
            return str(consolidated)
        except Exception as e:
            logger.error(f"Error creating consolidated summary: {str(e)}")
            # Fallback to simple concatenation
            return "\n\n".join([f"Document: {doc['file_name']} - {doc['summary']}" for doc in document_summaries])
