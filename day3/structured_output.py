from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal, Optional

class SQLOutput(BaseModel):
    sql : str
    explanation : str = Field(description='this should have explanation of the answer generated')
    operation_type : Literal["INSERT","DELETE","SELECT","UPDATE"]
    tables_used : list[str]
    filters_used : Optional[list[str]]
    clarity : int = Field("rate the user question on the clarity" , ge=1, le=10 )

load_dotenv()

client = OpenAI()


while True:
    user_input = input("ask your question: ")
    if user_input == 'exit':
        break
    response = client.responses.parse(model='gpt-5.6-sol',
                            input=user_input,
                            text_format = SQLOutput)
    
    result = response.output_parsed
    print(result.sql)
    print(result.explanation)
    print(result.operation_type)
    print(result.tables_used)
    print(result.filters_used)
    print(result.clarity)
