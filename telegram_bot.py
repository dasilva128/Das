# telegram_bot.py
from telegram import Bot
from telegram.error import TelegramError
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, bot_token, target_channel):
        self.bot = Bot(token=bot_token)
        self.target_channel = target_channel

    async def send_proxies(self, proxies):
        if not proxies:
            logger.info("No proxies to send")
            return

        # ایجاد پیام با تاریخ و زمان
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"🌐 پروکسی‌های HTTP جدید (مناسب ایران) - {current_time}:\n\n"
        for proxy in proxies:
            message += f"🔹 IP: {proxy['ip']}\n🔌 پورت: {proxy['port']}\n⏱ پینگ: {proxy['ping']}ms\n\n"
        
        try:
            await self.bot.send_message(chat_id=self.target_channel, text=message)
            logger.info(f"Sent {len(proxies)} proxies to {self.target_channel}")
        except TelegramError as e:
            logger.error(f"Error sending message to {self.target_channel}: {e}")