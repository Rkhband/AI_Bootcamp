from dotenv import load_dotenv
from openai import OpenAI
import json 
from tools import get_stock_details, currency_conversion_rate

load_dotenv()

client = OpenAI()


# def get_stock_details(stock_code:str):
#     prices  = {"INFY" : 100 , "TCS" : 200}
#     return prices[stock_code]

my_tools = [
    {
        "type": "function",
        "name": "get_stock_details",
        "description": "Get the current stock price for a given stock. returns stock name and latest price in INR.",
        "parameters": {
            "type": "object",
            "properties": {
                "stock_code": {
                    "type": "string",
                    "description": "NSE stock code for a given stock"
                }
            },
            "required": ["stock_code"]
        }
    },
    {
            "type": "function",
            "name": "currency_conversion_rate",
            "description": "use this function to get currency conversion rate from INR to any other currency",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_currency": {
                        "type": "string",
                        "description": "to_currency in which conversion rate is required from INR"
                    }
                },
                "required": ["to_currency"]
            }
        
    }
]

response = client.responses.create(model='gpt-5.6-sol',
                        input = "what is the stock price of Infosys in USD",
                        tools=my_tools)

 #input= 'what is the stock price of Infosys in USD',
response_id = response.id

tool_mapping = {'get_stock_details': get_stock_details , 'currency_conversion_rate' : currency_conversion_rate}
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

    if not tool_outputs:
        break

    response = client.responses.create(model='gpt-5.6-sol',
                        input = tool_outputs,
                        previous_response_id = response_id,
                        tools=my_tools)
    response_id = response.id

print(response.output_text)



#print(stock_price)


