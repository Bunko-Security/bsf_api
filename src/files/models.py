from sqlalchemy import (Column, ForeignKey, Integer, String, Date, DateTime, 
                        UniqueConstraint)

from datetime import datetime

from src.database import Base


class Files(Base):
    __tablename__ = 'files'
    
    file_id = Column('file_id', Integer, primary_key=True)
    user_from = Column('user_from', String, ForeignKey('users.login', ondelete='cascade'), nullable=False)
    filename = Column('filename', String, nullable=False)
    file_path = Column('file_path', String, nullable=False)
    upload_date = Column('upload_date', DateTime, nullable=False, default=datetime.now())
    delete_date = Column('delete_date', Date, nullable=False)
    

class FileUsers(Base):
    __tablename__ = 'file_users'
    
    file_user_id = Column('file_user_id', Integer, primary_key=True)
    user_to  = Column('user_to', String, ForeignKey('users.login', ondelete='cascade'), nullable=True)
    secret_key = Column('secret_key', String, nullable=False)
    file_id = Column('file_id', Integer, ForeignKey('files.file_id', ondelete='cascade'), nullable=False)
   
    __table_args__  = (UniqueConstraint('user_to', 'file_id', postgresql_nulls_not_distinct=True, name='unique_fileid_for_user'),)
