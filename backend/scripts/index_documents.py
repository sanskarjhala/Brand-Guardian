import os
import glob
import logging
from dotenv import load_dotenv

load_dotenv(override=True)

# document loaders and splitters
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Azure cpomponents
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch

# setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("indexer")


def index_docs():
    """
    Reads the PDF's , chunks them , and upload them to AZure AI Search
    """

    # Define the paths , we look for data folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir, "data")

    # cheack the envrioment varialbles
    logger.info("=" * 60)
    logger.info("Environment Configuration Check : ")
    logger.info("=" * 60)

    # validate the required variables
    required_vars = [
        "GITHUB_OPENAI_URL",
        "GITHUB_MODEL_API_KEY",
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_API_KEY",
        "AZURE_SEARCH_INDEX_NAME",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environments Varibles : {missing_vars}")
        logger.error(
            f"Please check your .env file and ensure all the variables are set"
        )
        return

    # Initialize the embedding model : turns text into vectors
    try:
        logger.info(f"Initializing Azure Open AI Embeddings ...")
        embeddings = OpenAIEmbeddings(
            model=os.getenv("GITHUB_EMBEDDING_MODEL"),
            openai_api_key=os.getenv("GITHUB_MODEL_API_KEY"),
            openai_api_base=os.getenv("GITHUB_OPENAI_URL"),
        )

        logger.info("Embedding model initalized successfully")
    except Exception as e:
        logger.error(f"Failed to Initialized Embeddings : {str(e)}")

    # Initialzed the Azure Search
    try:
        logger.info(f"Initializing Azure AI Search Vector Store ...")
        vector_store = AzureSearch(
            azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            azure_search_key=os.getenv("AZURE_SEARCH_API_KEY"),
            index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
            embedding_function=embeddings.embed_query,
        )
        logger.info("Embedding model initalized successfully")
    except Exception as e:
        logger.error(f"Failed to Initialized Embeddings : {str(e)}")

    #  Find the PDF FILES
    pdf_files = glob.glob(os.path.join(data_folder, "*.pdf"))
    if not pdf_files:
        logger.warning(
            f"No PDF's found in {data_folder}. Please ADd Files or cheack the Path"
        )
    logger.info(
        f"Found {len(pdf_files)} PDF's to process : {[os.path.basename(f) for f in pdf_files]}"
    )

    all_splits = []

    # process each pdf
    for pdf_path in pdf_files:
        try:
            logger.info(f"Loading :{os.path.basename(pdf_path)}.....")
            loader = PyPDFLoader(pdf_path)
            raw_docs = loader.load()

            # chunking
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )

            splits = text_splitter.split_documents(raw_docs)
            for split in splits:
                split.metadata["source"] = os.path.basename(pdf_path)

            all_splits.extend(splits)
            logger.info(f"Split into {len(splits)} chunks")

        except Exception as e:
            logger.error(
                f"---- Chunking Or Failed to process {pdf_path} , error : {str(e)}"
            )

        # Upload Azure AI Search Index
        if all_splits:
            logger.info(
                f"Uploading {len(all_splits)} chunks to Azure AI Search Index '{os.getenv("AZURE_SEARCH_INDEX_NAME")}'"
            )
            try:
                # Azure Searrch accept batches automatically via this method
                vector_store.add_documents(documents=all_splits)
                logger.info("=" * 60)
                logger.info(f"Indexing Is complte Knowledge base is ready")
                logger.info(f"Total Chunks Indexed : {len(all_splits)}")
                logger.info("=" * 60)
            except Exception as e:
                logger.error(
                    f"Failed to Upload the documents to azure search : {str(e)}"
                )
                logger.error(f"Please Check Azure Search Configuration and Try Again")

        else:
            logger.warning("No Documents were processed")


if __name__ == "__main__":
    index_docs()
