import logging
import json
from google.cloud import logging as cloud_logging
import os

# Initialize Google Cloud Logging client
cloud_logging_client = cloud_logging.Client()
cloud_handler = cloud_logging.handlers.CloudLoggingHandler(cloud_logging_client)


# Custom JSON Formatter for Structured Logging
class JSONFormatter(logging.Formatter):
    """JSON formatter for the logging util"""

    def format(self, record):
        log_record = {
            "severity": record.levelname,
        }
        if isinstance(record.msg, dict):
            # If user passed a dict, merge it directly
            log_record.update(record.msg)
        else:
            log_record["message"] = record.getMessage()
        return json.dumps(log_record)


formatter = JSONFormatter()
cloud_handler.setFormatter(formatter)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

if "K_SERVICE" in os.environ:  # Detect if running in Cloud Run
    logger.addHandler(cloud_handler)
else:
    # for local development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Log initialization message
logger.info(
    {
        "message": "Logging configuration initialized",
        "environment": "Cloud Run" if "K_SERVICE" in os.environ else "Local",
    }
)
