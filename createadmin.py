import getpass
import base64
import asyncio

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

from src.database import async_session_maker
from src.users.service import create_user
from src.users.schemas import UserCreate

class PasswordMismatchMaxAttempts(Exception):
    pass


async def main():
    login: str = input('Введите логин: ')
    password = getpass.getpass('Введите пароль: ')
    try_count = 3
    while try_count > 0:
        if password != getpass.getpass('Повторите пароль: '):
            print('Пароли не совпадают!')
        else:
            break
        try_count -= 1
    else:
        raise PasswordMismatchMaxAttempts
    hash_key = base64.b64encode(get_random_bytes(22)).decode()
    hash_sha256 = SHA256.new(hash_key.encode())
    hash_sha256.update(f'{password}&{login}'.encode())
    hash = hash_sha256.hexdigest()
    decrypt_key = hash[0: len(hash) // 2]
    auth_hash = hash[len(hash) // 2: len(hash)]
    rsa_keys = RSA.generate(2048)
    priv_key = rsa_keys.export_key(passphrase=decrypt_key, pkcs=8, protection=False).decode()
    pub_key = rsa_keys.public_key().export_key().decode()
    user = UserCreate(
        login = login,
        username = login,
        hash_key = hash_key,
        auth_hash = auth_hash,
        priv_key = priv_key,
        pub_key = pub_key,
        is_admin = True
    )
    async with async_session_maker() as db:
        await create_user(user, db)
    

if __name__ == '__main__':
    asyncio.run(main())

