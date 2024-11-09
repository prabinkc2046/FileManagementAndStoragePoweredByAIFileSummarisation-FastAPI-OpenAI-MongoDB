# Get value from environment variable
from  environment.get_env_variable import TOKEN_SECRET_KEY, TOKEN_ACCESS_EXPIRES_MINUTES, TOKEN_ALGORITHM

# define a list of file type that is accepted
ALLOWED_FILE_TYPES = {
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx"
}

# Secret key and algorithm for JWT
class JWT:
    SECRET_KEY = TOKEN_SECRET_KEY
    ALGORITHM = TOKEN_ALGORITHM
    ACCESS_TOKEN_EXPIRES_MINUTES = TOKEN_ACCESS_EXPIRES_MINUTES