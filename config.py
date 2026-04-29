import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")