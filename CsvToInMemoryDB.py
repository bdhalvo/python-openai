import openai
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text


def df_to_temp_db(df, table):
    engine = create_engine('sqlite:///:memory:')
    df.to_sql(name=table, con=engine, index=False)

    # with temp_db.connect() as conn:
    #     # with block auto closes the connection
    #     result = conn.execute(text('SELECT YEAR_ID, SUM(SALES) FROM Sales GROUP BY YEAR_ID'))
    #     # print(result.all())
    return engine


def csv_to_df(filename):
    dataframe = pd.read_csv(filename)
    return dataframe


def create_table_definition_prompt(df, table_name):
    ### sqlite SQL tables, with its properties:
    # Table(field1, field2, etc)
    #
    ### A query to get the total sales by quarter
    # SELECT
    fixed_prompt = '''### sqlite SQL tables, with its properties:
    #
    # {}({})
    #
    '''.format(table_name, ','.join(str(col) for col in df.columns))
    return fixed_prompt


def prompt_input():
    nlp_input = input("Enter the info you want: ")
    return nlp_input


def combine_prompts(fixed_prompt, query_prompt):
    query_init_string = f'### A query to answer: {query_prompt}\nSELECT'
    # print(definition + query_init_string)
    return fixed_prompt+query_init_string


def handle_response(response):
    query = response['choices'][0]['text']
    if query.startswith(' '):
        query = 'SELECT' + query
    return query


if __name__ == '__main__':
    df = csv_to_df('sales_data_sample.csv')
    # print(create_table_definition(csv_to_temp_db('sales_data_sample.csv')))
    in_mem_db = df_to_temp_db(df, 'Sales')
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    fixed_sql_prefix = create_table_definition_prompt(df, 'Sales')
    nlp_text = prompt_input()
    prompt = combine_prompts(fixed_sql_prefix, nlp_text)
    # print(prompt)
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=['#', ';']
    )

    query = handle_response(response)

    with in_mem_db.connect() as conn:
        result = conn.execute(text(query))
        print(result.fetchall())
