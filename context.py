from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# define OAuth2 scheme
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")
