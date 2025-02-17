from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("Endpoint")
key = os.getenv("Key")

cred = CognitiveServicesCredentials(key)
client = ComputerVisionClient(endpoint, cred)

def generate_caption_and_tags(image_path_or_url):
    
    try:
        
        if image_path_or_url.startswith("http://") or image_path_or_url.startswith("https://"):
            description_result = client.describe_image(image_path_or_url, max_descriptions=1, language="en")
            tags_result = client.tag_image(image_path_or_url)
        else:
            with open(image_path_or_url, "rb") as image_file:
                description_result = client.describe_image_in_stream(image_file, max_descriptions=1, language="en")
                image_file.seek(0)  # Reset the file pointer for the next request
                tags_result = client.tag_image_in_stream(image_file)

#Extract caption
        caption = "No caption generated"
        if description_result.captions:
            caption = description_result.captions[0].text

#Extract tags
        tags = [tag.name for tag in tags_result.tags[:]]  # Get all the tags

        return caption, tags
    except Exception as e:
        return f"Error processing caption and tags: {str(e)}", []


