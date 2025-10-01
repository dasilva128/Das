
# proxy_validator.py


import requests
import time
from proxy_manager import ProxyManager
from config import logger

class ProxyValidator:
    def __init__(self, timeout=10, max_latency=2000):
        self.timeout = timeout
        self.max_latency = max_latency
        self.test_urls = [
            "http://httpbin.org/get",
            "https://api.ipify.org?format=json",
            "http://checkip.dyndns.org"
        ]
        self.proxy_manager = ProxyManager()
        logger.info("Initialized ProxyValidator")

    def check_proxy(self, proxy):
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        for test_url in self.test_urls:
            try:
                start_time = time.time()
                response = requests.get(test_url, proxies=proxies, timeout=self.timeout)
                latency = (time.time() - start_time) * 1000
                if response.status_code == 200 and latency < self.max_latency:
                    logger.info(f"Proxy {proxy} is valid with latency {int(latency)}ms on {test_url}")
                    return True, latency
                logger.warning(f"Proxy {proxy} failed on {test_url}: status={response.status_code}, latency={int(latency)}ms")
            except Exception as e:
                logger.error(f"Proxy {proxy} failed on {test_url}: {e}")
        return False, None

    def validate_proxies(self):
        proxies = self.proxy_manager.get_proxies()
        valid_proxies = []
        logger.info(f"Validating {len(proxies)} proxies")
        for proxy in proxies:
            is_valid, latency = self.check_proxy(proxy)
            if is_valid:
                valid_proxies.append((proxy, latency))
        logger.info(f"Found {len(valid_proxies)} valid proxies")
        return valid_proxies