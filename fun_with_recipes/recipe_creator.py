import os
import openai
import re
import requests
import shutil
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
test_title = 'Ham, Turkey, Egg and Cheese Sandwich'


def create_dish_prompt(list_of_ingredients):
    prompt = f'Create a detailed recipe based on only the following ingredients: {", ".join(list_of_ingredients)}.\n' \
           + f'Additionally, assign a title starting with "Recipe Title: " to this recipe'

    return prompt


def dalle2_prompt(recipe_title):
    prompt2 = f'{recipe_title}, professional food photography, 15mm, studio lighting'
    return prompt2


def extract_title(recipe):
    return re.findall('^.*Recipe Title: .*$', recipe, re.MULTILINE)[0].strip().split('Recipe Title: ')[-1]


def save_ai_image(image_url, filename):
    # URL -> pic.png
    image_res = requests.get(image_url, stream=True)
    if image_res.status_code == 200:
        with open(filename, 'wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print('Error loading image')

    return image_res.status_code


img_response = openai.Image.create(
                prompt=dalle2_prompt(test_title),
                n=1,
                size='256x256')

img_url = img_response['data'][0]['url']
print(img_url)

save_ai_image(img_url, 'example_download.png')
# print(create_dish_prompt(['ham', 'turkey', 'eggs', 'bread']))
