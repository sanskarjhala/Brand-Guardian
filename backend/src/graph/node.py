import json
import os
import logging
import re
from typing import Dict, Any, List

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# Importing the State Schema
from src.graph.state import VideoAuditState, ComplinaceIssue

# import service
from src.services.video_indexer import VideoIndexerService  # have to create this file

# configure the logger
logger = logging.getLogger("brand-gaurdian")
logging.basicConfig(level=logging.INFO)

# Node-1 : Indexer
#  function Responsible for for converting videeo to text
def index_video_node(state: VideoAuditState) -> Dict[str, any]:
    """Downlads the youtube video from the urlUpoad to the Azure video Indexer and extracts the insights

    Args:
        state (VideoAuditState): the state of the agentic flow

    Returns:
        Dict[str , any]:
    """

    video_url = state.get("video_url")
    video_id = state.get("video_id", "vid_demo")

    logger.info(f"---- [Node:Indexer] ---- Processing : {video_url}")

    local_filename = "temp_audit_video.mp4"

    try:
        vi_service = VideoIndexerService()

        # Downaload the youtube -- using yt-dlp
        if "youtube.com" in video_url or "youtu.be" in video_url:
            local_path = vi_service.download_yotube_video(
                video_url, output_path=local_filename
            )
        else:
            raise Exception("Please Provide a valid Youtube URL for this seat")

        # upload the video
        azure_video_id = vi_service.upload_video(
            local_path, video_name=video_id
        )  # have to check this
        logger.info(f"Upload Success. Azure ID : {azure_video_id}")

        # clean up
        if os.path.exists(local_path):
            os.remove(local_path)

        # wait
        raw_insights = vi_service.wait_for_processing(azure_video_id)

        # extract
        clean_data = vi_service.extract_data(raw_insights)
        logger.info(f"---- [Node:Indexer] ---- Extraction Complete")
        return clean_data

    except Exception as e:
        logger.error(f"---- [Node:Indexer] ---- Video Indexer failed: {str(e)}")
        return {
            "error": [str(e)],
            "final_status": "FAIL",
            "transcript": "",
            "ocr_text": [],
        }


# Node-2 : Compliance Auditor
def audio_content_node(state: VideoAuditState) -> Dict[str, Any]:
    """Performs Retriveal Augmented Generation to audit the content - brand video

    Args:
        state (VideoAuditState): _description_

    Returns:
        Dict[str ,Any]: _description_
    """

    logger.info(f"---- [NODE: Auditor] Quering the knowledge base & LLM")
    transcript = state.get("transcript", "")

    if not transcript:
        logger.warning("Node Transcript available. Skipping Audit .....")
        return {
            "final_result": "FAIL",
            "final_report": "Audit Skipped Because video processing failed (No Transcipt)",
        }

    # initaize clients
    llm = ChatOpenAI(
        model=os.getenv("GITHUB_CHAT_MODEL"),
        openai_api_key=os.getenv("GITHUB_MODEL_API_KEY"),
        openai_api_base=os.getenv("GITHUB_OPENAI_URL"),
        temperature=0.0,
    )

    embeddings = OpenAIEmbeddings(
        model=os.getenv("GITHUB_EMBEDDING_MODEL"),
        openai_api_key=os.getenv("GITHUB_MODEL_API_KEY"),
        openai_api_base=os.getenv("GITHUB_OPENAI_URL"),
    )

    vector_store = AzureSearch(
        azure_search_endpoint=os.getenv(),
        azure_search_key=os.getenv(),
        index_name=os.getenv(),
        embedding_function=embeddings.embed_query,
    )

    # RAG Retirval
    ocr_text = state.get("ocr_text", "")
    query_text: f"{transcript} {" ".join(ocr_text)}"
    docs = vector_store.similarity_search(query_text, k=4)
    retrived_rules = "\n\n".join([doc.page_content for doc in docs])

    system_promt = f"""
        Your are the senior brand compliance auditor 
        OFFCIAL REGULARITY RULES:
        {retrived_rules}
        INSTRUCTION:
        1. Analyze the Transcript and OCT text below.
        2. Identify ANY violations of the rules.
        3. Return Strictly JSON in th following format:
            {{
            "compliance_results : [
                {{
                    "category" : "Claim Validation",
                    "severity" : "CRITICAL"
                    "description" : "Exaplanation of the validation..."
                }}        
            ],
            "status" : "FAIL",
            "final_report" : "Summary of findings..."
            }}
        if No violation are found, set "status" to "PASS" and "compliance_results" to [].
        """

    user_message = f"""
        VIDEO_METADATA : {state.get("video_metadata" , {})}
        TRANSCRIPT : {transcript}
        ON-SCREEN TEXT (OCR) : {ocr_text}
    """

    try:
        response = llm.invoke(
            [SystemMessage(content=system_promt), HumanMessage(content=user_message)]
        )

        content = response.content

        # HAve to check this one
        if "```" in content:
            content = re.search(r"```(?:json)?(.?)```", content, re.DOTALL).group(1)
        audit_data = json.loads(content.strip())

        return {
            "compliance_result": audit_data.get("compliance_results", []),
            "final_status": audit_data.get("status", "FAIL"),
            "final_report": audit_data.get("final_report", "No report generated"),
        }

    except Exception as e:
        logger.error(f"System Error in Auditor Node : {str(e)}")
        # logging the raw response
        logger.error(
            f"Raw LLM response : {response.content if "response" in  locals() else " None"}"
        )
        return {"errors": [str(e)], "final_status": "FAIL"}
