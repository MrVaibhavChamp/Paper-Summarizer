import dropbox
import pathway as pw
import os
from dotenv import load_dotenv
from common.embedder import embeddings, index_embeddings
from common.prompt import prompt
from pathway.xpacks.llm.parsers import ParseUnstructured
from pathway.xpacks.llm.splitters import TokenCountSplitter
load_dotenv()

# Initialize Dropbox client with your access token
dbx = dropbox.Dropbox(app_key = os.environ["DROPBOX_APP_KEY"],
                      app_secret=os.environ["DROPBOX_APP_SECRET"],
                      oauth2_access_token=os.environ.get("DROPBOX_ACCESS_TOKEN"),
                      oauth2_refresh_token=os.environ["DROPBOX_REFRESH_TOKEN"])

def fetch_pdf_files_from_dropbox():
    pdf_files = []
    try:
        # List files in the "LLM" folder
        for entry in dbx.files_list_folder("/LLM").entries:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith('.pdf'):
                # Download PDF file
                _, response = dbx.files_download("/LLM/" + entry.name)
                pdf_files.append(response.content)
    except dropbox.exceptions.ApiError as e:
        print(f"Error fetching PDF files from Dropbox: {e}")
    return pdf_files


def run(host, port):
    # Given a user search query
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    # Fetch PDF files from Dropbox
    # input_data = fetch_pdf_files_from_dropbox()
    dropbox_folder_path = os.environ.get("DROPBOX_ACCESS_TOKEN")
    
    # # Real-time data coming from external unstructured data sources like a PDF file
    input_data = pw.io.fs.read(
        dropbox_folder_path,
        mode="streaming",
        format="binary",
        autocommit_duration_ms=50)
    
    # Chunk input data into smaller documents
    parser = ParseUnstructured()
    documents = input_data.select(texts=parser(pw.this.data))
    documents = documents.flatten(pw.this.texts)
    documents = documents.select(texts=pw.this.texts[0])

    splitter = TokenCountSplitter()
    documents = documents.select(chunks=splitter(pw.this.texts))
    documents = documents.flatten(pw.this.chunks)
    documents = documents.select(chunk=pw.this.chunks[0])

    # Fetch PDF files from Dropbox
    # pdf_files = fetch_pdf_files_from_dropbox()
    
    # # Process each PDF file
    # documents = []
    # for pdf_content in pdf_files:
    #     # Parse PDF content into smaller documents
    #     parser = ParseUnstructured()
    #     parsed_documents = parser(pdf_content)
    #     documents.append(parsed_documents)
    
    # # Split documents into chunks
    # splitter = TokenCountSplitter()
    # chunks = []
    # for doc in documents:
    #     doc_chunks = splitter(doc)
    #     chunks.append(doc_chunks)
    

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = embeddings(context=documents, data_to_embed=pw.this.chunk)

    # Construct an index on the generated embeddings in real-time
    index = index_embeddings(embedded_data)

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()


class QueryInputSchema(pw.Schema):
    query: str
