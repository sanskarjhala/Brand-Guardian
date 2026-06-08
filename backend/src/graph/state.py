import operator
from typing import Annotated , List , Dict , Optional , Any , TypedDict

#  define the schema fior a single compilance result
# Error report -- If there is any issiue its is flag under this
class ComplinaceIssue(TypedDict):
    '''
    This is for the report Schema. This how the report should be generated
    '''
    category : str
    description : str # specific detasils of this violation
    severity : str # CRITICAL | WARNING
    timestamp : Optional[str]


#  GLOBAL STATE GRAPH
# this defines the state that gets passed arounf in the agentict worfflow
class VideoAuditState(TypedDict):
    '''
    Defines the data schema for lannggraph execution content
    Main Container : holds all the information about the audit right from the initial state to final report
    '''
    #  input parameters
    video_url : str
    video_id : str

    # ingestion and extraction data
    local_file_path : Optional[str]
    video_metadata : Dict[str , Any] # {"duration" : 15 , "resolution" : "1080p"}
    transcript : Optional[str] # fully extracted speech-to-text
    ocr_text : List[str]

    # analysis ouput
    # Stores the list of all the violation found by the AI
    compliance_results  : Annotated[List[ComplinaceIssue] , operator.add]

    # final deliverables
    final_status : str # PASS | FAIL
    final_report : str # markdown format

    # system obervability
    # errors : API TimeOut , system Level errors
    errors : Annotated[List[str] , operator.add]




