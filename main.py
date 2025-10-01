# proxy.py 
import os
import asyncio
from telegram.ext import Application, CommandHandler
from config import TELEGRAM_TOKEN, PROXY_SITES, logger
from proxy_scraper import ProxyScraper
from proxy_manager import ProxyManager
from proxy_validator import ProxyValidator
from scheduler import Scheduler
from telegram_bot import TelegramBot

async def start(update, context):
    logger.info(f"User {update.effective_user.id} started the bot")
    await update.message.reply_text("به ربات جمع‌آوری پروکسی خوش آمدید! از /scrape برای دریافت پروکسی‌های سالم استفاده کنید.")

async def scrape(update, context):
    user_id = update.effective_user.id
    logger.info(f"User {user_id} requested proxy scraping")
    await update.message.reply_text("در حال جمع‌آوری و بررسی پروکسی‌ها، لطفاً صبر کنید...")
    
    try:
        scraper = ProxyScraper(PROXY_SITES, ping_threshold=2000)
        proxies = scraper.scrape_proxies()
        
        proxy_manager = ProxyManager()
        for proxy in proxies:
            proxy_manager.add_proxy(proxy["ip"], proxy["port"])
        proxy_manager.save_proxies()
        
        validator = ProxyValidator()
        valid_proxies = validator.validate_proxies()
        
        if valid_proxies:
            proxy_list = "\n".join([f"{proxy} (پینگ: {int(latency)} میلی‌ثانیه)" for proxy, latency in valid_proxies])
            await update.message.reply_text(f"تعداد {len(valid_proxies)} پروکسی سالم یافت شد:\n{proxy_list}")
            logger.info(f"Sent {len(valid_proxies)} valid proxies to user {user_id}")
        else:
            await update.message.reply_text("هیچ پروکسی سالمی یافت نشد.")
            logger.warning(f"No valid proxies found for user {user_id}")
    except Exception as e:
        await update.message.reply_text("خطایی رخ داد. لطفاً دوباره تلاش کنید.")
        logger.error(f"Error in scrape command: {e}")

async def main():
    logger.info("Starting the bot")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scrape", scrape))
    
    bot = TelegramBot(TELEGRAM_TOKEN, target_channel=os.getenv("TELEGRAM_CHAT_ID", "@reahoora"))
    scraper = ProxyScraper(PROXY_SITES, ping_threshold=2000)
    scheduler = Scheduler(interval=3600, scraper=scraper, bot=bot)
    
    logger.info("Bot is running...")
    try:
        await app.initialize()
        await app.start()
        
        # Start scheduler as a task
        scheduler_task = asyncio.create_task(scheduler.start())
        
        await app.run_polling(poll_interval=1.0, timeout=10, close_loop=False)
    except KeyboardInterrupt:
        logger.info("Shutting down due to KeyboardInterrupt.")
        scheduler.stop()
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        scheduler.stop()
    finally:
        try:
            scheduler.stop()
            await scheduler_task  # Wait for scheduler to complete
            await app.stop()
            await app.shutdown()
            logger.info("Bot stopped and shutdown completed")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            logger.warning("An event loop is already running. Using existing loop.")
            loop.create_task(main())
        else:
            loop.run_until_complete(main())
    except RuntimeError as e:
        logger.error(f"Event loop error: {e}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())