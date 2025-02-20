import configparser
from gradio_client import Client, handle_file
import json
import os

def connect_with_hf_space(prompt, hf_space_endpoint, hf_dataset_endpoint):
    client = Client(hf_space_endpoint)
    obtained_images = client.predict(text_prompt=prompt, image_prompt=None, prompt_type="Text", nofimages_to_show=5, api_name="/predict")

    images_paths_list = []
    for current_image in obtained_images:
        images_paths_list.append(hf_dataset_endpoint + os.path.basename(current_image['image']))

    return images_paths_list

def lambda_handler(event, context):
    config = configparser.ConfigParser()
    config.read('config.cfg')

    prompt = event['queryStringParameters']['query']
    hf_space_endpoint = config['CLIENT']['hf_space_endpoint']
    hf_dataset_endpoint = config['CLIENT']['hf_dataset_endpoint']

    images_paths_list = connect_with_hf_space(prompt, hf_space_endpoint, hf_dataset_endpoint)

    return {
       'statusCode': 200,
       'body': json.dumps(images_paths_list)
    }
