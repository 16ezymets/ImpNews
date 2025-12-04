from functools import wraps
from sql_database import SessionLocal
import logging

logger = logging.getLogger(__name__)


def db_session(*, commit=True, rollback_on_error=True, close=True):
    """
    A universal decorator for working with databases.

    Params:
        - commit: automatically commit changes
        - rollback_on_error: rollback if necessary
        - close: automatically close the session
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(self, update, context, *args, **kwargs):
            db = SessionLocal()
            try:
                result = await func(self, update, context, db, *args, **kwargs)

                if commit:
                    db.commit()

                return result

            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")

                if rollback_on_error:
                    db.rollback()

                if update and hasattr(update, 'message'):
                    try:
                        await update.message.reply_text(f"❌ Ошибка: {str(e)[:100]}")
                    except Exception as e:
                        logger.error(f"Error in {func.__name__}: {e}")

                raise

            finally:
                if close:
                    db.close()

        return wrapper

    return decorator
