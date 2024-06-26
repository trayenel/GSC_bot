from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.sql import exists

engine = create_engine("sqlite:///./sqlite.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Chats(Base):
    __tablename__ = "chats"
    chat_id = Column(Integer, nullable=False, primary_key=True)
    link = Column(String, nullable=True, default=None)
    lang = Column(String, nullable=True)
    isReported = Column(Boolean, nullable=False, default=0)

    def __repr__(self):
        return f"<id(id={self.chat_id}, link={self.link}, lang={self.lang}, isReported={self.isReported})>"


Base.metadata.create_all(engine)

session = Session()


def addUser(usersTable, message_chat_id, user_lang):
    insert_stmt = insert(usersTable).values(chat_id=message_chat_id, lang=user_lang)
    do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["chat_id"])
    session.execute(do_nothing_stmt)
    session.commit()


def upsertLink(usersTable, message_chat_id, message_text):
    insert_stmt = insert(usersTable).values(chat_id=message_chat_id, link=message_text)
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["chat_id"], set_={"link": insert_stmt.excluded.link}
    )
    session.execute(upsert_stmt)
    session.commit()


def upsertReport(usersTable, message_chat_id, value):
    insert_stmt = insert(usersTable).values(chat_id=message_chat_id, isReported=value)
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["chat_id"], set_={"isReported": insert_stmt.excluded.isReported}
    )
    session.execute(upsert_stmt)
    session.commit()


def selectLink(linkTable, chat_id):
    link = session.query(linkTable).where(linkTable.chat_id == chat_id)
    return link[0].link


def upsertLang(usersTable, message_chat_id, language):
    insert_stmt = insert(usersTable).values(chat_id=message_chat_id, lang=language)
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["chat_id"], set_={"lang": insert_stmt.excluded.lang}
    )
    session.execute(upsert_stmt)
    session.commit()


def selectLang(userTable, chat_id):
    lang = session.query(userTable).where(userTable.chat_id == chat_id)
    return lang[0].lang


def selectReport(userTable, chat_id):
    isReported = session.query(userTable).where(userTable.chat_id == chat_id)
    return isReported[0].isReported


def checkUser(userTable, chat_id):
    return session.query(exists().where(userTable.chat_id == chat_id)).scalar()


def userLangChecker(table, message, log):
    if not checkUser(table, message.chat.id):
        log.warning(f"Chat id {message.chat.id} not yet in database.")
        addUser(table, message.chat.id, message.from_user.language_code)
        session.commit()
        log.info(
            f"Chat id {message.chat.id} added to database with default langauge: {message.from_user.language_code}."
        )

    lang = selectLang(table, message.chat.id)

    log.info(f"Chat id {message.chat.id} lang retrieved: {lang}")
    return lang
