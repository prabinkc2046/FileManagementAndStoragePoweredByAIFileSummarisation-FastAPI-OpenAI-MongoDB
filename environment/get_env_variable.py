from dotenv import load_dotenv
import os

# load environment variable 
load_dotenv()

# Load the API key from .env file
load_dotenv()

# access the required environment variables
MONGODB_PATH=os.getenv("MONGODB_PATH")
DB_NAME=os.getenv("DB_NAME")
TOKEN_SECRET_KEY=os.getenv("TOKEN_SECRET_KEY")
TOKEN_ALGORITHM=os.getenv("TOKEN_ALGORITHM")
TOKEN_ACCESS_EXPIRES_MINUTES=int(os.getenv("TOKEN_ACCESS_EXPIRES_MINUTES"))



