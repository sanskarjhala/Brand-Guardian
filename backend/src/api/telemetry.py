import os
import logging
from azure.monitor.opentelemetry import configure_azure_monitor
from dotenv import load_dotenv

load_dotenv(override=True)

# create a dedicated logger
logger = logging.getLogger("brand-guadian.telemetry")


def setup_telemetry():
    """
    Initializes Azure Monitor OpenTelemetry
    Tracks: HTTP requests, databse queries, errors, performance metrices
    Sends this data to azure monitor

    It auto captures every API request
    No need to manullay log eaxh point

    """

    # retrive the conncetion string
    connnection_string = os.getenv("APPICATIONINSIGHTS_CONNECTION_STRING")
    # Check if it configured or not
    if not connnection_string:
        logger.warning("No instrumentation key found. Telemetry is DISABLED")

    # configure the azure monitor
    try:
        configure_azure_monitor(
            connnection_string=connnection_string, logger_name="brand-guardian-tracing"
        )
        logger.info("Azure Monitor tracking Enabled and connnected")
    except Exception as e:
        logger.error(f"Failed to inintailze azure monitor : {str(e)}")
    