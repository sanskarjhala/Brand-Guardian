# FASTAPI APP

import uuid
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv(override=True)

# Initialze the tele,metry part here
from backend.src.api.telemetry import setup_telemetry

setup_telemetry()

# Import the workflow graph
from backend.src.graph.workflow import app as compliance_graph

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api-server")


# create the fastapi application
app = FastAPI(
    title="Brand Guardian AI API",
    description="Api for auditing Video content Against the brand compliance rules",
    version="1.0.0",
)

# defining the data models

class AuditRequest(BaseModel):
    """
        Define the Expected Structure of incoming API requests
        Example valid request:
    """
    