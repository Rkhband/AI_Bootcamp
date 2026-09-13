from bharatstock import BharatStock
import pandas as pd
import psycopg
from sqlalchemy import create_engine

def get_stock_details(stock_code:str):
    """
    call this function to get stock price details in INR

    args : NSE stock code for a company 

    returns company name and stock price details in INR
    """
    client = BharatStock(api_key="xxxxx")
    # A single stock, with latest price + derived metrics
    stock = client.stocks.get(stock_code)
    return stock.company_name, stock.latest_price


def price_conversion(price_in_inr:int , to_currency:str) :
    """
    use this function to convert price from INR to any other currency

    args : price_in_inr that needs to be converted , to_currency in which price needs to be converted

    returns converted price
    """
    rate = {"USD" : 0.5 , "EUR" : 0.1}
    return price_in_inr * rate[to_currency]


def currency_conversion_rate(to_currency:str) :
    """
    use this function to get currency conversion rate from INR to any other currency

    args : to_currency in which conversion rate is required from INR

    returns conversion rate 
    """
    rate = {"USD" : 0.5 , "EUR" : 0.1}
    return rate[to_currency]


#postgresql+psycopg://USERNAME:PASSWORD@HOST:PORT/DATABASE

engine = create_engine(
    "postgresql+psycopg://postgres@localhost:5432/postgres"
)

def execute_query(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

def list_tables():
    query = '''
        select table_name from information_schema.tables
        where table_schema = 'public';
        '''
    table_list = execute_query(query)
    return table_list

def get_schema(table_name):
    query = f'''
            SELECT
    table_name ,       
    column_name,
    data_type
    FROM information_schema.columns
    where table_schema= 'public' and table_name = '{table_name}'
    ORDER BY ordinal_position;
        '''
    schema = execute_query(query)
    return schema
#print(currency_conversion_rate('EUR'))

#get_stock_details('TCS')

#print(list_tables())

