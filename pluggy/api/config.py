import os

class Config:
    PLUGGY_API_URL =  os.getenv('PLUGGY_API_URL') or 'https://api.pluggy.ai'