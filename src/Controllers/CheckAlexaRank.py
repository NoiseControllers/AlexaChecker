from queue import Queue
from threading import Thread

from bs4 import BeautifulSoup


from src.Controllers.ProxyController import ProxyController
from src.Controllers.Requests import requests_get
from src.Utils.StringClean import clean


class CheckAlexaRank(Thread):
    def __init__(self, queue: Queue, output_list: list, proxy_controller: ProxyController or None):
        self._queue = queue
        self._output_list = output_list
        self._proxy_controller = proxy_controller
        self._base_url = "https://www.alexa.com/siteinfo/"
        super().__init__()

    def run(self) -> None:
        while True:
            url = self._queue.get()

            if url is None:
                break

            print(f"[+] Checking {url}")
            self.check_alexa_rank(url=url)
            self._queue.task_done()

    def check_alexa_rank(self, url: str):

        final_url = self._base_url + url
        while True:
            if self._proxy_controller is None:
                resp = requests_get(url=final_url)
            else:
                resp = requests_get(url=final_url, proxies=self._proxy_controller.get_next_proxy(), timeout=15)

            if resp is None or resp.status_code != 200:
                if resp is not None:
                    print(f"[DEBUG] {final_url} STATUS CODE {str(resp.status_code)}")
                else:
                    print(f"[DEBUG] {final_url} RESP IS NONE")

                continue
            else:
                break

        bs4 = BeautifulSoup(resp.content, "lxml")

        try:
            alexa_rank = clean(bs4.find("div", class_="rankmini-rank").get_text())
        except AttributeError:
            alexa_rank = None

        if alexa_rank is None:
            try:
                alexa_rank = clean(bs4.find("p", class_="big data").get_text())
            except AttributeError:
                alexa_rank = 100000000

        self._output_list.append((url, alexa_rank))
