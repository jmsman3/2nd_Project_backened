import requests
from django.conf import settings

def upload_image_to_imgbb(image_file):
    """Uploads an image to ImgBB and returns the image URL."""
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": settings.IMGBB_API_KEY,
        "image": image_file
    }
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        return response.json()['data']['url']
    else:
        raise Exception('Image upload failed: ' + response.text)
