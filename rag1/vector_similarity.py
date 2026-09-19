from openai import OpenAI
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

client = OpenAI()
def get_embeddings(text):
    response = client.embeddings.create(model='text-embedding-3-small',
                            input= text,
                            dimensions=300)
    return response.data[0].embedding

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


query = 'Where can I reset my login credentials'

query_embedding = get_embeddings(query)

similarity = cosine_similarity([query_embedding],doc_embeddings)

print(similarity)

