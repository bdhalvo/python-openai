import openai
from dotenv import load_dotenv
import os
import pandas as pd

# load_dotenv()
# openai.api_key = os.getenv('OPENAI_API_KEY')

df = pd.read_csv('sales_data_sample.csv')
# note: pd.read_sql, read_sqlquery, and read_sqltable all exist on pd as well

# What was the total sum of sales per quarter
# --> SELECT SUM(SALES) FROM table WHERE....

# so, anyway, let's make this df into a SQL in-memory database