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

#records = collection.get(ids=["id1"], include= ['metadatas', 'documents'])

#records = collection.get(where={"doc_name": 'insurance_doc.pdf'})

question = 'Where can I reset my login credentials'

question_embedding =  get_embeddings(question)

records  = collection.query(query_embeddings=question_embedding, n_results=5 )
print(records)
