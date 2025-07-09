from db import Base
from sqlalchemy import Column, Integer, String, Boolean, Text


class Sites(Base):
    __tablename__ = "sites"
    __table_args__ = {"schema": "raw"}

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(50))
    name = Column(String(200))
    cid = Column(String(26))
    manager = Column(String(36))
    submanager = Column(String(36))
    host = Column(Boolean, default=False)
    devteam = Column(String(100))
    lifetime = Column(Integer)
    state = Column(String(100))
    url = Column(Text)
