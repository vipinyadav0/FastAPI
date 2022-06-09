from .database import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text




class Posts(Base):
    __tablename__ = "dbposts"
    
    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String(100), nullable = False)
    content = Column(String(1000), nullable = False)
    published = Column(Boolean, server_default="TRUE", nullable = False) 
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable = False)
    
#this is under db_schemas