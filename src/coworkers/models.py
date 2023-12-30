from sqlalchemy import (Column, ForeignKey, String)
from sqlalchemy.orm import relationship

from src.database import Base


class Coworkers(Base):
    __tablename__ = 'coworkers'

    user_from = Column('user_from', String, ForeignKey('users.login', ondelete='cascade'), nullable=False, primary_key=True)
    user_to  = Column('user_to', String, ForeignKey('users.login', ondelete='cascade'), nullable=False, primary_key=True)
