from sqlalchemy import  create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    """
    Table 'users'.
    Stores user information and monitoring settings.

    Attributes:
        id: Unique database record ID (Primary Key, auto-increment)
        telegram_id: User's unique Telegram ID
        username: Telegram username (without @), can be None
        min_reactions: Minimum reactions threshold for notifications (default: 1000)
        channels: List of channels the user is tracking (many-to-many relationship)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    min_reactions = Column(Integer, default=1000)

    channels = relationship(
        "Channel",
        secondary="user_channels",
        backref="users"
    )


class Channel(Base):
    """
    Table 'channels'.
    Stores channel information for monitoring.

    Attributes:
        id: Unique database record ID (Primary Key)
        channel_username: Channel's username or identifier
        channel_title: Display name/title of the channel
        is_active: Whether the channel is active for monitoring (default: True)
    """
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    channel_username = Column(String, unique=True, index=True)
    channel_title = Column(String)
    is_active = Column(Boolean, default=True)


class UserChannel(Base):
    """
    Association table 'user_channels' for user-channel relationships.
    Implements many-to-many relationship between User and Channel models.

    Attributes:
        id: Unique database record ID (Primary Key, auto-increment)
        user_id: Reference to User.telegram_id (Foreign Key)
        channel_id: Reference to Channel.id (Foreign Key)
    """
    __tablename__ = "user_channels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'), index=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), index=True)


class SentPost(Base):
    """
    Table 'sent_posts'.
    Tracked posts that have been sent to users.
    Prevents duplicate notifications for the same post.

    Attributes:
        id: Unique database record ID (Primary Key, auto-increment)
        user_id: ID of the user who received the notification
        channel_id: ID of the channel where the post was found
        post_id: ID of the Telegram post/message
        sent_at: Timestamp when the post was sent (Unix timestamp)
    """
    __tablename__ = "sent_posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    channel_id = Column(Integer, index=True)
    post_id = Column(Integer, index=True)
    sent_at = Column(Integer)