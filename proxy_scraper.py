# proxy_scraper.py
import re
import requests
from bs4 import BeautifulSoup
from ping3 import ping
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='bot.log',
    format='%(asctime)s %(levelname)s:%(message)s'
)
logger = logging.getLogger(__name__)

class ProxyScraper:
    def __init__(self, proxy_websites, ping_threshold):
        self.proxy_websites = proxy_websites
        self.ping_threshold = ping_threshold
        self.http_pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})"

    def test_ping(self, host):
        try:
            response_time = ping(host, timeout=2, unit="ms")
            if response_time is None or response_time > self.ping_threshold:
                logger.debug(f"Proxy {host} failed ping test or ping too high: {response_time}")
                return None
            logger.debug(f"Proxy {host} passed ping test: {response_time}ms")
            return response_time
        except Exception as e:
            logger.debug(f"Error pinging {host}: {e}")
            return None

    def scrape_proxies(self):
        proxies = []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        logger.info(f"Starting proxy scrape from {len(self.proxy_websites)} websites")

        for url in self.proxy_websites:
            try:
                logger.info(f"Scraping website: {url}")
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code != 200:
                    logger.error(f"Failed to fetch {url}: Status {response.status_code}")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                matches = re.findall(self.http_pattern, text)
                logger.info(f"Found {len(matches)} potential proxies in {url}")
                for ip, port in matches:
                    ping_time = self.test_ping(ip)
                    if ping_time:
                        proxies.append({"ip": ip, "port": port, "ping": ping_time})
                        logger.info(f"Valid proxy: {ip}:{port} with ping {ping_time}ms")
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")

        logger.info(f"Total valid proxies found: {len(proxies)}")
        return sorted(proxies, key=lambda x: x["ping"])[:10]