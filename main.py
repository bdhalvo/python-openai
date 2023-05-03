import openai
from dotenv import load_dotenv
import os
import pandas as pd


def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(
                model='text-davinci-003',
                prompt='Give me two reasons to learn OpenAI API with Python',
                max_tokens=300)

    print(response['choices'][0]['text'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
