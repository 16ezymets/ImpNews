import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telethon import TelegramClient
from telethon.tl.types import Message, MessageReactions, User as tgUser, Chat

from sql_database import *
from db_utils import *
from config import API_ID, API_HASH, BOT_TOKEN, DEFAULT_MIN_REACTIONS

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

telethon_client = TelegramClient('monitor_session', API_ID, API_HASH)


class TelegramMonitorBot:
    """Main bot class for monitoring Telegram channels."""

    def __init__(self):
        self.application = None
        self.is_monitoring = False
        self.monitoring_start_times = {}

    @db_session(commit=True)  # Auto-commit enabled
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """Handler for /start command - user registration."""
        user_id = update.effective_user.id
        username = update.effective_user.username

        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            user = User(telegram_id=user_id, username=username)
            db.add(user)  # Auto-commit will be done by decorator

        welcome_msg = f"""👋 Hello, {update.effective_user.first_name}!
        
🤖 I'm a Telegram channel monitor bot.
                    
📋 Available commands:
/add_channel @username - add channel
/my_channels - show my channels  
/remove_channel @username - remove channel
/set_min_reactions 1000 - set reaction threshold
/start_monitoring - start monitoring
/stop_monitoring - stop monitoring
                    
📊 To start, add a channel:
/add_channel @bbc_russian"""

        await update.message.reply_text(welcome_msg)

    @db_session(commit=True)
    async def add_channel(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """Handler for /add_channel command."""
        if not context.args:
            await update.message.reply_text("Usage: /add_channel @username")
            return

        channel_username = context.args[0].replace('@', '')
        user_id = update.effective_user.id

        try:
            async with telethon_client:
                entity = await telethon_client.get_entity(channel_username)

                if isinstance(entity, tgUser):
                    await update.message.reply_text(
                        f"❌ @{channel_username} is a user, not a channel!\n"
                        "Add only public channels."
                    )
                    return

                elif isinstance(entity, Chat):
                    await update.message.reply_text(
                        f"❌ @{channel_username} is a group, not a channel!\n"
                        "Add only public channels."
                        "Or try to use /add_private_channel"
                    )
                    return

                elif hasattr(entity, 'restricted') and entity.restricted:
                    await update.message.reply_text(
                        f"⚠️ Chanel @{channel_username} is a private channel.\n"
                        "Make sure the bot is added as member."
                        "Or try to use /add_private_channel"
                    )
                    return

                channel_title = getattr(entity, 'title', channel_username)

            user = db.query(User).filter(User.telegram_id == user_id).first()
            if not user:
                user = User(telegram_id=user_id, username=update.effective_user.username)
                db.add(user)

            channel = db.query(Channel).filter(
                Channel.channel_username == channel_username
            ).first()

            if not channel:
                channel = Channel(
                    channel_username=channel_username,
                    channel_title=channel_title
                )
                db.add(channel)

            if channel in user.channels:
                await update.message.reply_text(f"❌ @{channel_username} already added!")
            else:
                user.channels.append(channel)
                await update.message.reply_text(f"✅ @{channel_username} added!\nTitle: {channel_title}")

        except Exception as e:
            logger.error(f"Error in add_channel: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
            raise

    @db_session(commit=True)
    async def add_private_channel(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """Handler for /add_private_channel command."""
        if not context.args:
            await update.message.reply_text(
                "Usage:\n"
                "(ID) /add_private -1001234567890\n"
                "or\n"
                "(Join link) /add_private t.me/joinchat/ABC123def456"
            )
            return

        identifier = context.args[0]
        user_id = update.effective_user.id

        try:
            async with telethon_client:
                entity = await telethon_client.get_entity(identifier)

                if not isinstance(entity, Channel):
                    await update.message.reply_text("❌ That is not a channel!")
                    return

                channel_title = entity.title
                channel_id = entity.id

                if entity.username:
                    channel_username = entity.username
                else:
                    channel_username = f"private_{abs(channel_id)}"

                try:
                    test_msg = await telethon_client.get_messages(entity, limit=1)
                    if not test_msg:
                        await update.message.reply_text("⚠️  I can't read messages. Please check your permissions.")
                except Exception as e:
                    await update.message.reply_text("❌ No read laws in this channel!")
                    logger.error(f'Error reading private channel messages: {e}')
                    return

                channel = db.query(Channel).filter(
                    Channel.channel_username == channel_username
                ).first()

                if not channel:
                    channel = Channel(
                        channel_username=channel_username,
                        channel_title=channel_title,
                        is_active=True
                    )
                    db.add(channel)

                user = db.query(User).filter(User.telegram_id == user_id).first()
                if not user:
                    user = User(telegram_id=user_id, username=update.effective_user.username)
                    db.add(user)

                if channel not in user.channels:
                    user.channels.append(channel)
                    await update.message.reply_text(f"✅ @{channel_username} added!\nTitle: {channel_title}")
                else:
                    await update.message.reply_text(f"❌ @{channel_username} already added!")

        except Exception as e:
            logger.error(f"Private channel error: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")

    @db_session(commit=True)
    async def remove_channel(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """Handler for /remove_channel command."""
        if not context.args:
            await update.message.reply_text("Usage: /remove_channel @username")
            return

        channel_username = context.args[0].replace('@', '')
        user_id = update.effective_user.id

        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            await update.message.reply_text("❌ User not found. Use /start first.")
            return

        channel = db.query(Channel).filter(
            Channel.channel_username == channel_username
        ).first()

        if not channel:
            await update.message.reply_text(f"❌ Channel @{channel_username} not found!")
            return

        if channel in user.channels:
            user.channels.remove(channel)
            await update.message.reply_text(f"✅ Removed @{channel_username} from your list!")
        else:
            await update.message.reply_text(f"❌ Channel @{channel_username} wasn't added!")

    @db_session(commit=False)
    async def my_channels(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """Handler for /my_channels command - using relationships."""
        user_id = update.effective_user.id

        user = db.query(User).filter(User.telegram_id == user_id).first()

        if not user:
            await update.message.reply_text("❌ User not found. Use /start first.")
            return

        user_channels = user.channels

        if not user_channels:
            await update.message.reply_text("📭 No channels added yet.")
            return

        channels_list = "\n".join([
            f"• @{channel.channel_username or 'unknown'} ({channel.channel_title or 'No title'})"
            for channel in user_channels
        ])
        await update.message.reply_text(f"📊 Your channels ({len(user_channels)}):\n\n{channels_list}")

    @db_session(commit=True)
    async def set_min_reactions(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """Handler for /set_min_reactions command."""
        if not context.args or not context.args[0].isdigit():

            user_id = update.effective_user.id
            user = db.query(User).filter(User.telegram_id == user_id).first()
            current = user.min_reactions if user else DEFAULT_MIN_REACTIONS

            await update.message.reply_text(
                f"Usage: /set_min_reactions <number>\nCurrent: {current}"
            )
            return

        min_reactions = int(context.args[0])
        user_id = update.effective_user.id

        if min_reactions < 0:
            await update.message.reply_text("❌ Reaction count cannot be negative!")
            return
        if min_reactions > 10e6:
            await update.message.reply_text("❌ That's too many reactions!")
            return

        user = db.query(User).filter(User.telegram_id == user_id).first()
        if user:
            user.min_reactions = min_reactions
            await update.message.reply_text(f"✅ Threshold set: {min_reactions} reactions")
        else:
            await update.message.reply_text("❌ User not found!")

    async def start_monitoring(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /start_monitoring command."""
        user_id = update.effective_user.id

        if self.is_monitoring:
            await update.message.reply_text("🔍 Monitoring already running!")
            return

        self.monitoring_start_times[user_id] = int(datetime.now().timestamp())

        self.is_monitoring = True
        asyncio.create_task(self.monitor_channels())
        await update.message.reply_text("🚀 Monitoring started!")

    async def stop_monitoring(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /stop_monitoring command."""
        self.is_monitoring = False
        await update.message.reply_text("⏹️ Monitoring stopped!")

    async def monitor_channels(self):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                db = SessionLocal()
                try:
                    users = db.query(User).all()

                    for user in users:
                        for channel in user.channels:
                            await self.check_channel_posts(db, user, channel)

                    db.commit()

                except Exception as e:
                    db.rollback()
                    logger.error(f"DB error in monitoring: {e}")
                finally:
                    db.close()

                await asyncio.sleep(300)

            except Exception as e:
                logger.error(f"Critical monitoring error: {e}")
                await asyncio.sleep(60)

    async def check_channel_posts(self, db, user, channel):
        """Check posts in specific channel."""
        try:
            start_time = self.monitoring_start_times.get(user.telegram_id)
            if not start_time:
                return

            async with telethon_client:
                messages = await telethon_client.get_messages(
                    channel.channel_username,
                    limit=10
                )

                for message in messages:
                    if not isinstance(message, Message):
                        continue

                    # Check if post was already sent
                    sent_post = db.query(SentPost).filter(
                        SentPost.user_id == user.telegram_id,
                        SentPost.channel_id == channel.id,
                        SentPost.post_id == message.id
                    ).first()

                    if sent_post:
                        continue

                    reactions_count = self.get_reactions_count(message)

                    if reactions_count >= user.min_reactions:
                        await self.send_popular_post(
                            user.telegram_id,
                            channel,
                            message,
                            reactions_count
                        )

                        sent_post = SentPost(
                            user_id=user.telegram_id,
                            channel_id=channel.id,
                            post_id=message.id,
                            sent_at=int(datetime.now().timestamp())
                        )
                        db.add(sent_post)
                        db.commit()

                    if hasattr(message, 'date') and message.date:
                        if message.date.timestamp() < start_time:
                            continue

        except Exception as e:
            logger.error(f"Error checking {channel.channel_username}: {e}")

    @staticmethod
    def get_reactions_count(message: Message) -> int:
        """Calculate total reaction count."""
        if not message.reactions:
            return 0

        if isinstance(message.reactions, MessageReactions):
            total = 0
            for reaction in message.reactions.results:
                total += reaction.count
            return total

    async def send_popular_post(self, user_id: int, channel: Channel,
                                message: Message, reactions_count: int):
        """Send popular post to user."""
        try:
            post_text = message.message or ""
            if len(post_text) > 4000:  # Telegram limit
                post_text = post_text[:3998] + "..."

            post_link = f"https://t.me/{channel.channel_username}/{message.id}"

            caption = (
                f"🔥 Popular post!\n\n"
                f"📢 Channel: {channel.channel_title}\n"
                f"👍 Reactions: {reactions_count}\n"
                f"🔗 Link: {post_link}\n\n"
                f"{post_text}"
            )

            await self.application.bot.send_message(
                chat_id=user_id,
                text=caption,
                disable_web_page_preview=True
            )

        except Exception as e:
            logger.error(f"Error sending post: {e}")

    def run(self):
        """Start the bot."""
        create_tables()

        self.application = Application.builder().token(BOT_TOKEN).build()

        handlers = [
            ("start", self.start),
            ("add_channel", self.add_channel),
            ("add_private_channel", self.add_private_channel),
            ("remove_channel", self.remove_channel),
            ("my_channels", self.my_channels),
            ("set_min_reactions", self.set_min_reactions),
            ("start_monitoring", self.start_monitoring),
            ("stop_monitoring", self.stop_monitoring),
        ]

        for command, handler in handlers:
            self.application.add_handler(CommandHandler(command, handler))

        print("🤖 Bot starting")
        self.application.run_polling()


if __name__ == "__main__":
    bot = TelegramMonitorBot()
    bot.run()
