from sqlalchemy import ( # type: ignore
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class TestModel(Base):
    __tablename__ = 'testtable'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    age = Column(Integer)
    base_template = Column(Text)


Index('test_index', TestModel.name, unique=True)
