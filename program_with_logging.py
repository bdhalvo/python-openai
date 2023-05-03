# Dataset based on #https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import openai

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
openai.api_key = os.environ['OPENAI_API_KEY']


def dataframe_to_database(df, table_name):
    """Convert a pandas dataframe to a database.
        Args:
            df (dataframe): pd.DataFrame which is to be converted to a database
            table_name (string): Name of the table within the database
        Returns:
            engine: SQLAlchemy engine object
    """
    engine = create_engine('sqlite:///:memory:', echo=False)
    df.to_sql(name=table_name, con=engine, index=False)
    return engine


def handle_response(response):
    query = response['choices'][0]['text']
    if query.startswith(' '):
        query = 'SELECT' + query
    return query


def execute_query(engine, query):
    with engine.connect() as conn:
        query_result = conn.execute(text(query))
        return query_result.fetchall()


def create_table_definition_prompt(df, table_name):
    static_prompt = '''### sqlite table, with its properties:
#
# {}({})
#
'''.format(table_name, ','.join(str(col) for col in df.columns))
    return static_prompt


def user_input():
    user_question = input('Tell OpenAI what you want to know about the data: ')
    return user_question


def combine_prompts(static_sql, user_query):
    final_user_input = f'### A query to answer: {user_query}\nSELECT'
    return static_sql + final_user_input


def send_to_openai(final_prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=final_prompt,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=['#', ';']
    )
    return response


if __name__ == '__main__':
    logging.info('Loading data...')
    df = pd.read_csv('data/sales_data_sample.csv')
    logging.info(f'Data Format: {df.shape}')

    logging.info('Converting to database...')
    database = dataframe_to_database(df, 'Sales')
    
    fixed_sql_prompt = create_table_definition_prompt(df, 'Sales')
    logging.info(f'Fixed SQL Prompt: {fixed_sql_prompt}')

    logging.info('Waiting for user input...')
    user_input = user_input()
    final_prompt = combine_prompts(fixed_sql_prompt, user_input)
    logging.info(f'Final Prompt: {final_prompt}')

    logging.info('Sending to OpenAI...')
    response = send_to_openai(final_prompt)
    proposed_query = response['choices'][0]['text']
    proposed_query_processed = handle_response(response)
    logging.info(f'Response obtained. Proposed sql query: {proposed_query_processed}')
    result = execute_query(database, proposed_query_processed)
    logging.info(f'Result: {result}')
    print(result)
