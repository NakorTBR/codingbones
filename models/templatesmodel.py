from sqlalchemy import ( # type: ignore
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
)

from .meta import Base

class TemplatesModel(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id')) # type: ignore
    template_header = Column(Text)
    base_template = Column(Text) # Main entry point
    class_template = Column(Text)
    method_template = Column(Text)



Index('id', TemplatesModel.id, unique=True)
