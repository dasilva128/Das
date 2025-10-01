# scraper.py 

import requests
from bs4 import BeautifulSoup
import re
import base64
from proxy_manager import ProxyManager
from config import logger

class ProxyScraper:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        logger.info("Initialized ProxyScraper")

    def scrape_freeproxy_world(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            if not table:
                logger.warning(f"No table found on {url}")
                return
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    self.proxy_manager.add_proxy(ip, port)
        except Exception as e:
            logger.error(f"Error scraping freeproxy.world: {e}")

    def scrape_hidemy_name(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="proxy__t") or soup.find("table")
            if not table:
                logger.warning(f"No table found on {url}")
                return
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    self.proxy_manager.add_proxy(ip, port)
        except Exception as e:
            logger.error(f"Error scraping hidemy.name: {e}")

    def scrape_proxynova(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", id="proxy_list") or soup.find("table")
            if not table:
                logger.warning(f"No table found on {url}")
                return
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip_script = cols[0].find("script")
                    if ip_script:
                        match = re.search(r'"([^"]+)"', ip_script.text)
                        if match:
                            ip = match.group(1)
                            try:
                                ip = base64.b64decode(ip).decode('utf-8')
                            except Exception as e:
                                logger.error(f"Error decoding IP {ip}: {e}")
                                continue
                        else:
                            logger.warning(f"No IP found in script for row: {row}")
                            continue
                    else:
                        ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    self.proxy_manager.add_proxy(ip, port)
        except Exception as e:
            logger.error(f"Error scraping proxynova: {e}")

    def scrape_free_proxy_cz(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", id="proxy_list")
            if not table:
                logger.warning(f"No table found on {url}")
                return
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip_script = cols[0].find("script")
                    if ip_script:
                        match = re.search(r'"([^"]+)"', ip_script.text)
                        if match:
                            ip_encoded = match.group(1)
                            try:
                                ip = base64.b64decode(ip_encoded).decode('utf-8')
                            except Exception as e:
                                logger.error(f"Error decoding IP {ip_encoded}: {e}")
                                continue
                        else:
                            logger.warning(f"No IP found in script for row: {row}")
                            continue
                    else:
                        ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    self.proxy_manager.add_proxy(ip, port)
        except Exception as e:
            logger.error(f"Error scraping free-proxy.cz: {e}")

    def scrape_ditatompel(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="table")
            if not table:
                logger.warning(f"No table found on {url}")
                return
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    self.proxy_manager.add_proxy(ip, port)
        except Exception as e:
            logger.error(f"Error scraping ditatompel: {e}")

    def scrape_spys_one(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="spy1x")
            if not table:
                logger.warning(f"No table found on {url}")
                return
            rows = table.find_all("tr")[2:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip_port = cols[0].text.strip()
                    if ":" in ip_port:
                        ip, port = ip_port.split(":")
                        self.proxy_manager.add_proxy(ip, port)
        except Exception as e:
            logger.error(f"Error scraping spys.one: {e}")

    def scrape_proxy_spider(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            if not table:
                logger.warning(f"No table found on {url}")
                return
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    self.proxy_manager.add_proxy(ip, port)
        except Exception as e:
            logger.error(f"Error scraping proxy-spider: {e}")

    def scrape_freeproxyupdate(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            if not table:
                logger.warning(f"No table found on {url}")
                return
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    self.proxy_manager.add_proxy(ip, port)
        except Exception as e:
            logger.error(f"Error scraping freeproxyupdate: {e}")

    def scrape_premiumproxy(self, url):
        try:
            logger.info(f"Scraping {url}")
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            if not table:
                logger.warning(f"No table found on {url}")
                return
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    self.proxy_manager.add_proxy(ip, port)
        except Exception as e:
            logger.error(f"Error scraping premiumproxy: {e}")

    def scrape_all(self, urls):
        logger.info("Starting to scrape all proxy sites")
        for url in urls:
            if "freeproxy.world" in url:
                self.scrape_freeproxy_world(url)
            elif "hidemy.name" in url:
                self.scrape_hidemy_name(url)
            elif "proxynova.com" in url:
                self.scrape_proxynova(url)
            elif "free-proxy.cz" in url:
                self.scrape_free_proxy_cz(url)
            elif "ditatompel.com" in url:
                self.scrape_ditatompel(url)
            elif "spys.one" in url:
                self.scrape_spys_one(url)
            elif "proxy-spider.com" in url:
                self.scrape_proxy_spider(url)
            elif "freeproxyupdate.com" in url:
                self.scrape_freeproxyupdate(url)
            elif "premiumproxy.net" in url:
                self.scrape_premiumproxy(url)
        self.proxy_manager.save_proxies()
        logger.info("Finished scraping all proxy sites")