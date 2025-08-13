import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
import os

load_dotenv()
NAME = os.getenv("CLOUD_NAME")
KEY = os.getenv("API_KEY")
SECRET = os.getenv("API_SECRET")
def uploadImage(imageId, studId):
    cloudinary.config( 
    cloud_name = NAME, 
    api_key = KEY, 
    api_secret = SECRET, 
    secure=True)
    # Upload an image
    upload_result = cloudinary.uploader.upload(imageId,
                                           public_id=studId)
    
    # Optimize delivery by resizing and applying auto-format and auto-quality
    optimize_url, _ = cloudinary_url(studId, fetch_format="auto", quality="auto")
    # Transform the image: auto-crop to square aspect_ratio
    auto_crop_url, _ = cloudinary_url(studId, width=500, height=500, crop="auto", gravity="auto")
    return auto_crop_url
