from dotenv import load_dotenv
from openai import OpenAI
import json 
from tools import get_stock_details, price_conversion

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
            "name": "price_conversion",
            "description": "use this function to convert price from INR to any other currency",
            "parameters": {
                "type": "object",
                "properties": {
                    "price_in_inr": {
                        "type": "number",
                        "description": "price_in_inr that needs to be converted"
                    },
                    "to_currency": {
                                     "type": "string",
                                            "description": "to_currency in which price needs to be converted"
                                        }
                },
                "required": ["price_in_inr","to_currency"]
            }
        }
]

response = client.responses.create(model='gpt-5.6-sol',
                        input= 'what is the stock price of Infosys in USD',
                        tools=my_tools)

tool_call = response.output[1]
args = json.loads(tool_call.arguments)
function_name  = tool_call.name

if function_name == 'get_stock_details':
    stock_price = get_stock_details(**args)

#print(stock_price)


call_id = tool_call.call_id
response_id = response.id

tool_output = [{"type": "function_call_output",
       "call_id": call_id,
       "output": str(stock_price)}]


response = client.responses.create(model='gpt-5.6-sol',
                        input= tool_output,
                        previous_response_id=response_id,
                        tools=my_tools)

print(response.output_text)
print(response.output)
