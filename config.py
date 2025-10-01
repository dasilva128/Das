# config.py
import logging
import os

# Telegram Bot Token
TELEGRAM_TOKEN = "5735916294:AAHLPFFE8GK3IYgGJ8brS0mAeOrK6-6t7vs"

# Proxy Sites
PROXY_SITES = [
    "https://www.freeproxy.world/?type=http&anonymity=&country=IR&speed=&port=&page=1",
    "https://hidemy.name/en/proxy-list/countries/iran",
    "https://www.proxynova.com/proxy-server-list/country-ir",
    "http://free-proxy.cz/en/proxylist/country/IR/all/ping/all",
    "https://www.ditatompel.com/proxy/country/ir",
    "https://spys.one/free-proxy-list/IR/",
    "https://proxy-spider.com/proxies/locations/ir-iran",
    "https://freeproxyupdate.com/iran-ir",
    "https://premiumproxy.net/top-country-proxy-list/IR-Iran/",
]

# Logging Configuration
LOG_FILE = "bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Also print logs to console
    ]
)
logger = logging.getLogger(__name__)