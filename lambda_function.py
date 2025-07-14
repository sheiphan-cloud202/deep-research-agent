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

    Args:
        event: The Lambda event object containing request information
        context: The Lambda context object containing runtime information

    Returns:
        dict: HTTP response in Lambda proxy integration format
    """

    try:
        # Log request information for debugging
        method = event.get("httpMethod", "Unknown")
        path = event.get("path", "Unknown")
        logger.info(f"Received event: {method} {path}")

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
