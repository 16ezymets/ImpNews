from unittest.mock import Mock
from bot import TelegramMonitorBot
from telethon.tl.types import MessageReactions


def test():
    """Test get_reactions_count method"""
    bot = TelegramMonitorBot()

    # Test 1: Message without reactions
    message1 = Mock()
    message1.reactions = None
    result1 = bot.get_reactions_count(message1)
    assert result1 == 0

    # Test 2: Message with reactions
    reaction = Mock()
    reaction.count = 5

    reactions = Mock(spec=MessageReactions)
    reactions.results = [reaction]

    message2 = Mock()
    message2.reactions = reactions
    result2 = bot.get_reactions_count(message2)
    assert result2 == 5

    print("✅ All tests passed!")


if __name__ == "__main__":
    test()
