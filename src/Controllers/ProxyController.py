from itertools import cycle


class ProxyController:
    def __init__(self, type_sock: str, proxies: list):
        self._type_sock = type_sock
        self._proxies = proxies
        self._cycle_proxies = cycle(self._proxies)

    def get_next_proxy(self) -> dict:
        proxy = next(self._cycle_proxies)
        proxies = {
            "http": f"{self._type_sock}://{proxy}",
            "https": f"{self._type_sock}://{proxy}"
        }

        return proxies

    def remove_proxy(self, proxy: str):
        pass
