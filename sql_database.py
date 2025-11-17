from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    """
    Table 'users' : (id, telegram_id, username, min_reactions)

    Columns types:
    id: int, telegram_id: int, username: string, min_reactions: int
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True) # Ex: @username
    min_reactions = Column(Integer, default=100)


class Channel(Base):
    """
    Table 'channel' : (id, channel_username, channel_title, is_active)

    Columns types:
    id: int, channel_username: str, channel_title: string, is_active: bool
    """
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    channel_username = Column(String, unique=True, index=True) # Ex: @channel
    channel_title = Column(String)
    is_active = Column(Boolean, default=True)


class UserChannel(Base):
    """
    Table 'channels' : (id, user_id, channel_id)

    Columns types:
    id: int, user_id: int, channel: int
    """
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    chanel_id = Column(Integer, index=True)


class SentPost(Base):
    """
    Table 'sent_posts' : (id, user_id, channel_id, post_id, sent_at)

    Columns types:
    id: int, user_id: int, channel_id: int, post_id: int, sent_at: int
    """
    __tablename__ = "sent_posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    channel_id = Column(Integer, index=True)
    post_id = Column(Integer, index=True)
    sent_at = Column(Integer) # timestamp

    @staticmethod
    def create_tables():
        """
        Creates all tables
        :return: None
        """
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def get_db():
        """
        Gets database if possible
        :return: Generator[Session, Any, None] | None
        """
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
