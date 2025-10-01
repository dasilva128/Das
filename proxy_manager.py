# proxy_manager.py
import json
import os
from config import logger

class ProxyManager:
    def __init__(self, file_path="proxies.json"):
        self.file_path = file_path
        self.proxies = []
        self.load_proxies()  # Load proxies on initialization
        logger.info(f"Initialized ProxyManager with file: {file_path}")

    def add_proxy(self, ip, port):
        proxy = f"{ip}:{port}"
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            logger.info(f"Added proxy: {proxy}")

    def save_proxies(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.proxies, f, indent=2)
            logger.info(f"Saved {len(self.proxies)} proxies to {self.file_path}")
        except Exception as e:
            logger.error(f"Error saving proxies: {e}")

    def load_proxies(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    self.proxies = json.load(f)
                logger.info(f"Loaded {len(self.proxies)} proxies from {self.file_path}")
            except Exception as e:
                logger.error(f"Error loading proxies: {e}")
        else:
            logger.warning(f"No proxy file found at {self.file_path}")
        return self.proxies

    def get_proxies(self):
        return self.proxies