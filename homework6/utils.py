import bcrypt
from schemes import User

def generate_passwd_hash(passwd: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def process_user(user: User):
    user.passwd = generate_passwd_hash(user.passwd)
    return user
