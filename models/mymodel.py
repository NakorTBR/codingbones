from sqlalchemy import ( # type: ignore
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


# Got caught up doing maintence work for a client.
# Need to make more useful model for testing.
class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


Index('my_index', MyModel.name, unique=True, mysql_length=255)
