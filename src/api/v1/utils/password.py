from passlib.context import CryptContext

class PasswordUtils:
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

  
    @classmethod
    def verify_password(cls,password: str, hashed_password: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, hashed_password)