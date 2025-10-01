# scheduler.py
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, interval, scraper, bot):
        self.interval = interval
        self.scraper = scraper
        self.bot = bot
        self.running = False

    async def job(self):
        try:
            proxies = self.scraper.scrape_proxies()  # از proxy_scraper.py
            await self.bot.send_proxies(proxies)
            logger.info("Scheduled job completed")
        except Exception as e:
            logger.error(f"Error in scheduled job: {e}")

    async def start(self):
        self.running = True
        logger.info(f"Scheduler started with interval {self.interval} seconds")
        while self.running:
            await self.job()
            await asyncio.sleep(self.interval)

    def stop(self):
        self.running = False
        logger.info("Scheduler stopped")