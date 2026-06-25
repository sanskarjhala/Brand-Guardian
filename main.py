"""
Main Exceution entry ponits fot he Compilnace QA Pipeline.

This file is the "control center" that starts and manages the entrire compliance audit workflow.
Think of it as the master switch that:

1 . Sets up the audit request
2. Runs The AI workflow
3. Displays the final compliance report

"""

import uuid
import logging
import json
from pprint import pprint

from dotenv import load_dotenv

load_dotenv(override=True)

from backend.src.graph.workflow import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d - %(message)s",
)

logger = logging.getLogger("brand-guardian-runner")


def run_cli_simulation():
    """
    Simulates a video compliance audit request

    This Function Orchestrates the entire audit Process
    - creates a unique session ID
    - Prepares The video URL and metadata
    - Runs it through the AI workflow
    - Displays the compliance results

    """

    # Step-1 : GENERATE THE SESSION ID - Creats a unique Identifier fot this audit session
    session_id = str(uuid.uuid4())
    logger.info(f"Strating Audit Session : {session_id}")

    # Step-2 : DEFINE INITIAL INPUT FOR THE
    intital_inputs = {
        # THE YOUTUBE ADD/VIDEO URL FOR COMPLIANCE CHECK
        "video_url": "",
        # THE SHORTHAND VIDEO-ID FOR TRACKING THE PROCESS
        "video_id": f"vide_{session_id[:8]}",
        # EMPTY LIST THAT WILL STORE COMPLIANCE VIOLATIONS FOUND
        # WILL BE POPULATED BY THE AUDITOR NODE
        "compliance_results": [],
        # EMPTY LIST FOR ANY ERRORS DUSRING THE PROCESSING
        "errors": [],
    }

    print(f"---- Initializing workflow ----")
    print(f"Input Payload : {json.dumps(intital_inputs , indent=2)}")

    try:
        final_state = app.invoke(intital_inputs)
        print(f" ------  Compliance Audit Report -------")
        print(f"Video ID : {final_state.get("video_id")}")
        print(f"Status : {final_state.get("final_state")}")
        print(" ------- VIOLATION DETECTED ---------")
        results = final_state.get("compliance_results", [])
        if results:
            for issue in results:
                print(
                    f" - [{issue.get('severity')}] [{issue.get("category")}] : [{issue.get("description")}]"
                )
        else:
            print("No violations Detected .....")
        print(f" ---- [FINAL REPORT] ---- {final_state.get("final_report")}")

    except Exception as e:
        logger.error(f"Worflow Execution Failed : {str(e)}")
        raise e


if __name__ == "__main__":
    run_cli_simulation()
