"""
This module defines the DAG : Directed Acyclic Graph that orchestrates the video compilance audiut process.
It connnects the nodes using the StateGraph from LanGgraph

START -> index_video_node -> audit_content_node -> END
"""

from langgraph.graph import StateGraph, END
from src.graph.state import VideoAuditState
from src.graph.node import index_video_node, audio_content_node

def create_graph():
    """
    Constructs and complies the LangGraph Workflow
    Returns: Complied Graph -> runnable graph object for execution
    """

    # Initialize the graph with state scherma
    workflow = StateGraph(VideoAuditState)

    # add the nodes
    workflow.add_node("indexer", index_video_node)
    workflow.add_node("auditor", audio_content_node)

    # define the Entry point
    workflow.set_entry_point("indexer")

    # define the edges
    workflow.add_edge("indexer", "auditor")
    workflow.add_edge("auditor", END)

    # Complie the graph
    app = workflow.compile()
    return app

# expose this runnable app
app = create_graph()
