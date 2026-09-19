import chromadb
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def get_embeddings(text):
    response = client.embeddings.create(model='text-embedding-3-small',
                            input= text,
                            dimensions=300)
    return response.data[0].embedding

db_client = chromadb.PersistentClient("./chroma_db")

collection = db_client.get_or_create_collection(name="demo_collection")

documents  = ["How can I change my password"
              , "databricks is a data and ai platform and uses spark as compute engine"
              , "snowflake is a data warehousing platform and has emreging as ened to end data and AI paltform"
              ,"GenAI is emerging field for data engineers"
              ,"Virat Kohli has awesome cover drive"
              ,"I love playing football"
              , "big data engineering has high salaries"
              ]
doc_embeddings = []

for text in documents:
    doc_embeddings.append(get_embeddings(text))

collection.add(
    ids=["id1", "id2", "id3","id4", "id5", "id6", "id7"],
    embeddings=doc_embeddings,
    documents=documents,
    metadatas= [{"doc_name" : 'hr_doc.pdf',"version" : 1 },{"doc_name" : 'hr_doc.pdf',"version" : 1 },{"doc_name" : 'hr_doc.pdf',"version" : 1 },
                {"doc_name" : 'insurance_doc.pdf',"version" : 1 },{"doc_name" : 'insurance_doc.pdf',"version" : 1 },{"doc_name" : 'insurance_doc.pdf',"version" : 1 },{"insurance_doc" : 'hr_doc.pdf',"version" : 1 } ] )

