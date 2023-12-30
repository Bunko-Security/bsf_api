from sqlalchemy import Column, String, Boolean

from src.database import Base

class Users(Base):
    __tablename__ = 'users'

    login = Column('login', String, nullable=False, primary_key=True)
    username = Column('username', String, nullable=False)
    hash_key = Column('hash_key', String, nullable=False)
    auth_hash = Column('auth_hash', String, nullable=False)
    priv_key = Column('priv_key', String, nullable=False)
    pub_key = Column('pub_key', String, nullable=False)
    avatar_path = Column('avatar_path', String, nullable=True)
    is_admin= Column('is_admin', Boolean, nullable=False, server_default='False')