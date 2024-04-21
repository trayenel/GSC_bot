from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import insert

engine = create_engine("sqlite:///./sqlite.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Links(Base):
    __tablename__ = "reportedLinks"
    chat_id = Column(Integer, nullable=False, primary_key=True)
    link = Column(String, nullable=False)

    def __repr__(self):
        return f"<id(id={self.chat_id}, link={self.link})>"


Base.metadata.create_all(engine)

session = Session()


def upsertLink(linkTable, message_chat_id, message_text):
    insert_stmt = insert(linkTable).values(chat_id=message_chat_id, link=message_text)
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["chat_id"], set_={"link": insert_stmt.excluded.link}
    )
    session.execute(upsert_stmt)
    session.commit()


def selectLink(linkTable, chat_id):
    link = session.query(linkTable).where(linkTable.chat_id == chat_id)
    return link[0].link
