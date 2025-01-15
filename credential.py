import os
import dotenv

def getPathEnv():
    dotenv.load_dotenv('.env')
    API_KEY = os.getenv('API-KEY')
    API_HASH = os.getenv('API-HASH')
    SESSION = os.getenv('SESSION')
    DATABASE = os.getenv('DATABASE')
    
    return API_KEY, API_HASH, SESSION, DATABASE
