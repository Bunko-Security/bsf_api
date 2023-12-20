from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def bcrypt_auth_key(
    login: str, auth_key: str
) -> str:
    return pwd_cxt.hash(auth_key + login)

def verify_auth_key(
    login: str, plain_auth_key: str, hashed_auth_key: str
) -> str:
    return pwd_cxt.verify(plain_auth_key + login, hashed_auth_key)
