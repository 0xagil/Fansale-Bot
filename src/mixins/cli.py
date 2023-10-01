from datetime import datetime
from termcolor import colored

class PrintableMixin:
    """Base class for all CLI classes"""
    def __init__(self, title: str, identifier: str):
        self.title: str = title
        self.identifier: str = identifier

    def _return_date(self) -> str:
        now = datetime.now()
        date_time_str = now.strftime("%d.%m.%Y %H:%M:%S.%f")[:-2]
        return date_time_str

    def _return_prefix(self) -> str:
        return f"[{self.title} - {self.identifier}] [{self._return_date()}] >> "

    def print_cli(self, text: str, color: str) -> None:
        """Prints in color"""
        print(self._return_prefix(), colored(text, color))
