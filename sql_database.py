from sqlalchemy import  create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    min_reactions = Column(Integer, default=1000)

    # Только один relationship
    channels = relationship(
        "Channel",
        secondary="user_channels",
        backref="users"
    )


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    channel_username = Column(String, unique=True, index=True)
    channel_title = Column(String)
    is_active = Column(Boolean, default=True)



class UserChannel(Base):
    __tablename__ = "user_channels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'), index=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), index=True)


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
    sent_at = Column(Integer)



def create_tables():
    """
    Creates all tables
    :return: None
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Creates and get database
    :return: Generator[Session, Any, None] | None
    """
    db = SessionLocal()
    return db