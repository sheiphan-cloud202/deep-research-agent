import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Set up logging for the application.
    """
    # Prevent logger from propagating to the root logger
    logger = logging.getLogger("deep_research_agent")
    logger.propagate = False
    logger.setLevel(level)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create a handler to write to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    # add the handlers to the logger
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

logger = setup_logging() 