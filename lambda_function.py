"""
AWS Lambda handler for the Deep Research Agent API.

This module provides the entry point for deploying the FastAPI application
to AWS Lambda using Mangum as the ASGI-to-Lambda adapter.
"""

import logging
import os

from mangum import Mangum

from deep_research_agent.api.main import app

# Configure logging for Lambda environment
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create the Mangum adapter
# Mangum converts FastAPI (ASGI) to Lambda handler format
handler = Mangum(app, lifespan="off")


def lambda_handler(event, context):
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

    # Log request information for debugging
    logger.info(f"Received event: {event.get('httpMethod', 'Unknown')} {event.get('path', 'Unknown')}")

    # Set any additional environment variables or configurations specific to Lambda
    # This is useful for distinguishing between local development and Lambda execution
    os.environ.setdefault("LAMBDA_EXECUTION", "true")

    try:
        # Call the Mangum handler which will process the FastAPI app
        response = handler(event, context)

        # Log successful response
        logger.info(f"Successfully processed request, status: {response.get('statusCode', 'Unknown')}")

        return response

    except Exception as e:
        # Log errors for CloudWatch debugging
        logger.error(f"Error processing request: {str(e)}", exc_info=True)

        # Return a proper error response
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            },
            "body": '{"error": "Internal server error"}',
        }
