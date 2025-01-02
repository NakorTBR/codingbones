from sqlalchemy import ( # type: ignore
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    String,
)

from sqlalchemy.orm import relationship, backref # type: ignore

from .meta import Base


class UsersModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(100))
    user_pass = Column(String(100)) # Obviously temp
    user_email = Column(String(255))
    user_join_date = Column(DateTime)

    templates = relationship('TemplatesModel', backref='user')


# Index('id', TemplatesModel.name, unique=True)