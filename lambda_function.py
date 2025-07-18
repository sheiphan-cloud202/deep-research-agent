"""
AWS Lambda handler for the Deep Research Agent API.

This module provides the entry point for deploying the FastAPI application
to AWS Lambda using Mangum as the ASGI-to-Lambda adapter.
"""

import json
import logging
import os
from typing import Any

from mangum import Mangum

from deep_research_agent.api.main import app

# Configure logging for Lambda environment
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create the Mangum adapter
# Mangum converts FastAPI (ASGI) to Lambda handler format
handler = Mangum(app, lifespan="off")


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    AWS Lambda handler function.

    This is the entry point that AWS Lambda will call when handling requests.
    It uses Mangum to adapt the FastAPI ASGI application to work with Lambda's
    event/context model.

    The handler supports two types of simplified events for local testing,
    in addition to the full AWS API Gateway proxy event:

    1. Generic Simplified Event: A dictionary containing `path`, `method`,
       and optionally `path_params`, `query_params`, and `body`. E.g.:
       {
           "path": "/research/{id}/respond",
           "method": "POST",
           "path_params": {"id": "123"},
           "body": {"response": "some answer"}
       }

    2. Legacy Simplified Event: A dictionary representing only the request body
       for a `POST` request to `/research`.

    Args:
        event: The Lambda event object containing request information.
               Can be a full API Gateway event or a simplified event.
        context: The Lambda context object containing runtime information

    Returns:
        dict: HTTP response in Lambda proxy integration format
    """
    # If this is not a full API Gateway event, treat it as a simplified event.
    if "httpMethod" not in event:
        logger.info("Simplified event detected. Wrapping for local testing.")

        # Generic simplified event format
        if "path" in event and "method" in event:
            path = event.get("path")
            method = event.get("method", "POST").upper()
            path_params = event.get("path_params")
            query_params = event.get("query_params")
            body = event.get("body", {})

            resource = path
            if path_params:
                resource_path = path
                for key, value in path_params.items():
                    if resource_path and value in resource_path:
                        resource_path = resource_path.replace(str(value), f"{{{key}}}")
                resource = resource_path

            event = {
                "httpMethod": method,
                "path": path,
                "resource": resource,
                "pathParameters": path_params,
                "queryStringParameters": query_params,
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "user-agent": "aws-lambda-test-simplified",
                },
                "body": json.dumps(body) if body is not None else None,
                "isBase64Encoded": False,
                "requestContext": {
                    "httpMethod": method,
                    "path": path,
                    "resourcePath": resource,
                    "accountId": "123456789012",
                    "apiId": "local-testing",
                    "stage": "test",
                    "requestId": "local-request",
                    "identity": {"sourceIp": "127.0.0.1"},
                },
                "stageVariables": None,
            }
        # Fallback for original simplified event (body for POST /research)
        else:
            logger.info("Legacy simplified event detected for POST /research.")
            event = {
                "httpMethod": "POST",
                "path": "/research",
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                "body": json.dumps(event),
                "isBase64Encoded": False,
                "requestContext": {
                    "httpMethod": "POST",
                    "path": "/research",
                    "resourcePath": "/research",
                    "accountId": "123456789012",
                    "apiId": "local-testing",
                    "stage": "test",
                    "requestId": "local-request",
                    "identity": {"sourceIp": "127.0.0.1"},
                },
                "resource": "/research",
                "pathParameters": None,
                "queryStringParameters": None,
                "stageVariables": None,
            }

    try:
        # Log request information for debugging
        method = event.get("httpMethod", "Unknown")
        path = event.get("path", "Unknown")
        logger.info(f"Received event: {method} {path}")

        # Log additional workflow-related information for monitoring
        if "/research/" in path and method == "POST":
            logger.info(
                "Research workflow request detected - workflow_context will be accessible via status endpoints"
            )
        elif "/status" in path:
            logger.info("Workflow status request - providing real-time progress information")

        # Set any additional environment variables or configurations specific to Lambda
        # This is useful for distinguishing between local development and Lambda execution
        os.environ.setdefault("LAMBDA_EXECUTION", "true")

        # Call the Mangum handler which will process the FastAPI app
        response = handler(event, context)

        # Ensure CORS headers are present
        if "headers" not in response:
            response["headers"] = {}

        response["headers"].update(
            {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
                "Content-Type": "application/json",
            }
        )

        # Log successful response
        status_code = response.get("statusCode", "Unknown")
        logger.info(f"Successfully processed request, status: {status_code}")

        return response

    except Exception as e:
        # Log errors for CloudWatch debugging
        logger.error(f"Error processing request: {str(e)}", exc_info=True)

        # Return a proper error response following the reference pattern
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            },
            "body": json.dumps({"error": "Internal server error", "message": str(e)}),
        }
