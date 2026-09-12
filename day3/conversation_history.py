from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

history = []
history.append({"role":"system","content":"You are an expert data engineer"})

# maintainining history using a list and roles.
while True:
    user_input = input("ask your question: ")
    if user_input == 'exit':
        break
    history.append({"role":"user","content": user_input })
    #print(history)
    response = client.responses.create(model='gpt-5.6-sol',
                            input=history)
    history.append({"role":"assistant","content": response.output_text })
    print(response.output_text)

# using reponse id 

# response_id = None
# while True:
#     user_input = input("ask your question: ")
#     if user_input == 'exit':
#         break
#     #print(history)
#     response = client.responses.create(model='gpt-5.6-sol',
#                             input=user_input,
#                             previous_response_id = response_id)
#     response_id = response.id

#     history.append({"role":"assistant","content": response.output_text })
#     print(response.output_text)

