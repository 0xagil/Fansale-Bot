import time
from typing import Tuple
from threading import Thread
import capsolver

from src.mixins.cli import PrintableMixin
from src.utils.types import CaptchaSite, Task, TargetOffer
from src.api.eventim_api import init_checkout_session
from src.api.fansale_api import reserve_tickets
from src.api.cookie_api import get_cookie
from settings import CAPSOLVER_KEY


class Bank(PrintableMixin):
    """The Bank stores and manages tokens of various types"""

    def __init__(self, name) -> None:
        self.bank: dict = {}
        self.paused: bool = False
        super().__init__(name, "")

        self.print_cli(f"Initialized {name}", "green")

    def clean_bank(self, key: str) -> None:
        """Removes old tokens from the bank"""
        token_amount_before = len(self.bank[key])
        self.bank[key] = [
            token for token in self.bank[key] if token["timestamp"] > time.time() - 100
        ]
        token_amount_after = len(self.bank[key])
        difference = token_amount_before - token_amount_after
        if difference > 0:
            self.print_cli(f"Removed {difference} old tokens", "yellow")

    def add_to_bank(self, token: str, key: str) -> None:
        """Adds a token to the bank"""
        self.bank[key].append({"token": token, "timestamp": time.time()})
        self.print_cli(f"Added 1 token to bank {key}", "magenta")

    def get_token(self, key: str) -> str:
        """Returns a token from the bank"""
        if len(self.bank[key]) == 0:
            return None
        return self.bank[key].pop(0)["token"]


class CaptchaBank(Bank):
    """The captcha bank stores and manages the captcha tokens"""

    def __init__(self, name, captcha_sites) -> None:
        super().__init__(name)
        self.captcha_sites = captcha_sites
        self.bank: dict = {site.url: [] for site in captcha_sites}

    def solve_captcha(self, url: str, site_key: str) -> Tuple[str, bool]:
        """Solves the captcha and returns the response and a boolean if the captcha was solved successfully"""
        capsolver.api_key = CAPSOLVER_KEY
        try:
            solution = capsolver.solve(
                {
                    "type": "ReCaptchaV2TaskProxyLess",
                    "websiteURL": url,
                    "websiteKey": site_key,
                }
            )
            response = solution["gRecaptchaResponse"]
            success = True
        except Exception as e:
            response = ""
            success = False
            self.identifier = url
            self.print_cli("Failed to solve captcha", "red")
        return response, success

    def run_worker(self, captcha_site: CaptchaSite):
        """Runs the captcha bank"""
        while True:
            captcha, success = self.solve_captcha(
                captcha_site.url, captcha_site.site_key
            )
            if success:
                self.add_to_bank(captcha, captcha_site.url)
                self.clean_bank(captcha_site.url)
                start_sleep = time.time()
                while time.time() - start_sleep < captcha_site.delay:
                    time.sleep(1)
                    if len(self.bank[captcha_site.url]) == 0:
                        break
            time.sleep(0.1)
            while self.paused:
                time.sleep(1)

    def start(self):
        """Starts the captcha bank"""
        threads = []
        for captcha_site in self.captcha_sites:
            t = Thread(target=self.run_worker, args=(captcha_site,))
            threads.append(t)
            t.start()
        [thread.join() for thread in threads]


class EventimBank(Bank):
    """The eventim bank stores and manages the eventim tokens"""

    def __init__(self, name, task_list) -> None:
        super().__init__(name)
        self.task_list = task_list
        self.bank: dict = {site.event_id: [] for site in task_list}

    def fetch_tokens(self, task: Task) -> Tuple[Tuple[str, str], bool]:
        """Fetches the eventim tokens and returns the response and a boolean if the tokens were fetched successfully"""
        try:
            xsrf_token, session_token = init_checkout_session(task)
            success = True
        except Exception:
            xsrf_token = ""
            session_token = ""
            success = False
            self.print_cli("Failed to solve captcha", "red")
        return (xsrf_token, session_token), success

    def run_worker(self):
        """Runs the captcha bank"""
        while True:
            for task in [task for task in self.task_list if task.active]:
                tokens, success = self.fetch_tokens(task)
                if success:
                    self.identifier = task.event_id
                    self.add_to_bank(tokens, task.event_id)
                    self.clean_bank(task.event_id)
            time.sleep(10)
            while self.paused:
                time.sleep(1)

    def start(self):
        """Starts the token bank"""
        Thread(target=self.run_worker).start()

class CookieBank(Bank):

    def __init__(self, name) -> None:
        super().__init__(name)
        self.bank: dict = {"cookies": []}

    def fetch_tokens(self) -> dict:
        """Fetches the fansale cookies and returns the response and a boolean if the tokens were fetched successfully"""
        cookies = {}
        good_cookies = False
        while not good_cookies:
            cookies = get_cookie()
            if cookies:
                good_cookies = self.check_cookie(cookies)
            else:
                time.sleep(1)
            time.sleep(1)
        return cookies
    
    def check_cookie(self, cookies):
        test_task = Task(
            event_id = "122",
            category = [],
            min_ticket = 1,
            fansale_url = "https://www.fansale.de",
            eventim_url = "",
            eventim_affiliate = "",
            active = True,
            location = ""
        )
        target_offer = TargetOffer(
            offer_id = "1212",
            tickets = "1212",
            ticket_name =  "1212",
            task = test_task
        )
        recaptcha = "1212"
        try:
            reserve_tickets(target_offer, recaptcha, cookies)
            return True
        except Exception as e:
            print(e)
            return False

    def run_worker(self):
        """Runs the cookie bank"""
        while True:
            cookies = self.fetch_tokens()
            self.add_to_bank(cookies, "cookies")
            self.clean_bank("cookies")
            time.sleep(40)
            while self.paused:
                time.sleep(1)

    def start(self):
        """Starts the cookie bank"""
        Thread(target=self.run_worker).start()
