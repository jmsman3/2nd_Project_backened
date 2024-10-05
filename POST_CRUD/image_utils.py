import requests

import cloudinary.uploader
from Social_Media_Project import settings

def upload_image_to_imgbb(image_file):
    api_key = '59c029e1206724ae1f2e3c30d278d10f'  
    url = 'https://api.imgbb.com/1/upload'
    payload = {
        'key'  : settings.IMGBB_API_KEY,
        'image': image_file.read(),
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json().get('data', {}).get('url')
    return None


def upload_video_to_cloudinary(video_file):
    try:
        # Upload video to Cloudinary
        response = cloudinary.uploader.upload_large(
            video_file, resource_type="video"
        )
        return response.get('url')
    except Exception as e:
        print(f"Video upload failed: {str(e)}")
        return None




# def upload_video_to_imgbb(video_file):

#     api_key = '59c029e1206724ae1f2e3c30d278d10f'  
#     url = 'https://api.imgbb.com/1/upload'  
#     payload = {
#         'key'  : settings.IMGBB_API_KEY,
#         'video': video_file.read(),
#     }
#     response = requests.post(url, data=payload)
#     if response.status_code == 200:
#         return response.json().get('data', {}).get('url')
#     return None
