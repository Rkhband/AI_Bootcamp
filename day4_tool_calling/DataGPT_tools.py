from openai import OpenAI
from dotenv import load_dotenv
from tools import execute_query , get_schema, list_tables
import json 

load_dotenv()

client = OpenAI()


schema = get_schema('orders')

my_tools = [
    {
        "type": "function",
        "name": "execute_query",
        "description": "use this tool to execute a sql on postgres db",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "sql query that has to be executed"
                }
            },
            "required": ["query"]
        }
    },
    {
            "type": "function",
            "name": "get_schema",
            "description": "use this tool to get schema of a table",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "ttable name for which schema is required"
                    }
                },
                "required": ["table_name"]
            }
        
    },
    {
                "type": "function",
                "name": "list_tables",
                "description": "use this tool to get the table list from database",
            
        }
]

response = client.responses.create(model='gpt-5.6-sol',
                        input = "give me top 5 products by sales",
                        tools=my_tools)

 #input= 'what is the stock price of Infosys in USD',
response_id = response.id

tool_mapping = {'execute_query': execute_query , 'get_schema' : get_schema , 'list_tables' : list_tables}
while True:
    tool_outputs = []
    llm_output = response.output
    for item in llm_output:
        if item.type == 'function_call':
            args = json.loads(item.arguments)
            function_name  = item.name
            print(function_name , args)
            call_function = tool_mapping[function_name]
            tool_result = call_function(**args)
            call_id = item.call_id
            tool_outputs.append({"type": "function_call_output",
                            "call_id": call_id,
                                "output": str(tool_result)})
            print(tool_outputs)
    if not tool_outputs:
        break

    response = client.responses.create(model='gpt-5.6-sol',
                        input = tool_outputs,
                        previous_response_id = response_id,
                        tools=my_tools)
    response_id = response.id

print(response.output_text)
