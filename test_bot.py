import pytest
from unittest.mock import Mock, AsyncMock
from telethon.tl.types import MessageReactions
from bot import TelegramMonitorBot


class TestTelegramMonitorBot:
    """Tests for TelegramMonitorBot methods"""

    @pytest.fixture
    def bot(self):
        """Create a bot instance for testing"""
        return TelegramMonitorBot()

    def test_no_reactions(self, bot):
        """Test 1: message without reactions"""
        message = Mock(reactions=None)
        result = bot.get_reactions_count(message)
        assert result == 0

    def test_reactions(self, bot):
        """Test 2: message with reactions"""
        reactions_list = [
            Mock(count=10),
            Mock(count=3),
            Mock(count=7)
        ]
        reactions = Mock(spec=MessageReactions, results=reactions_list)
        message = Mock(reactions=reactions)

        result = bot.get_reactions_count(message)
        assert result == 20

    def test_bot_initialization(self):
        """Test 3: bot initializes correctly"""
        bot = TelegramMonitorBot()
        assert bot.is_monitoring is False
        assert bot.monitoring_start_times == {}
        assert bot.application is None

    @pytest.mark.asyncio
    async def test_stop_monitoring(self, bot):
        """Test 4: stop_monitoring sets is_monitoring to False"""
        update = Mock()
        update.message = Mock()
        update.message.reply_text = AsyncMock()
        context = Mock()

        bot.is_monitoring = True
        await bot.stop_monitoring(update, context)
        assert bot.is_monitoring is False

        bot.is_monitoring = False
        await bot.stop_monitoring(update, context)
        assert bot.is_monitoring is False

    @pytest.mark.asyncio
    async def test_start_monitoring(self, bot):
        """Test 5: start_monitoring sets is_monitoring to True"""
        update = Mock()
        update.message = Mock()
        update.message.reply_text = AsyncMock()
        context = Mock()

        bot.is_monitoring = False
        await bot.start_monitoring(update, context)
        assert bot.is_monitoring is True

        bot.is_monitoring = True
        await bot.start_monitoring(update, context)
        assert bot.is_monitoring is True
