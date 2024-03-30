from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///./sqlite.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Links(Base):
    __tablename__ = 'reportedLinks'
    chat_id = Column(Integer, nullable=False)
    link = Column(String, nullable=False, primary_key=True)

    def __repr__(self):
        return f"<id(id={self.id}, link={self.link})>"

Base.metadata.create_all(engine)

session = Session()
