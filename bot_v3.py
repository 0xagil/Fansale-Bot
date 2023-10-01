from threading import Thread
import time
import datetime
import urllib.parse
import requests


from src.mixins.cli import PrintableMixin
from src.modules.scraper import Monitor
from src.modules.checkout import Checkout
from src.utils.bank import CaptchaBank, EventimBank, CookieBank
from src.utils.types import TargetOffer
from src.utils.utils import isNowInTimePeriod

from settings import CAPTCHA_SITES, TASK_LIST, TELEGRAM_BOT, CHAT_ID, THREAD_AMOUNT

with open("proxies.txt", "r", encoding="utf_8") as f:
    proxy_list = f.read().split("\n")

class Controller(PrintableMixin):
    """Controller of the Bot"""

    def __init__(self) -> None:
        self.ticket_blocking_mode = False
        self.proxie_mode = False
        self.cookie_injection_mode = True


        self.proxies: list = proxy_list
        self.old_offer_ids: list = []
        self.target_offer: TargetOffer
        self.thread_amount = THREAD_AMOUNT
        self.target_offer_found: bool = False
        self.bedtime: bool = False

        self.captcha_bank = CaptchaBank("CaptchaBank", CAPTCHA_SITES)
        self.eventim_bank = EventimBank("EventimBank", TASK_LIST)
        self.cookie_bank = CookieBank("CookieBank")
        self.checkout_instance = Checkout()

        super().__init__("Fansale Bot", "")

    def setup(self):
        """Starting the monitoring threads and the Captcha Bank"""

        Thread(target=self.captcha_bank.start).start()
        Thread(target=self.eventim_bank.start).start()
        Thread(target=self.cookie_bank.start).start()
        for i in range(self.thread_amount):
            scraper = Monitor(self.proxies, TASK_LIST, i, self)
            Thread(target=scraper.run).start()

    def reset(self):
        """Resets the Bot after the checkout finished"""
        self.target_offer = TargetOffer
        self.target_offer_found = False

    def send_confirmation_telegram(
        self, redirect_url: str, cookies: dict, ticket_name: str, location: str
    ) -> None:
        """Sends a confirmation message to the telegram group"""
        webid = cookies["webid"]
        webshop = cookies["webshop"]
        safe_url = urllib.parse.quote(redirect_url)
        text = f"✅ FansaleBot\n\n{location}\n{ticket_name}\n\nUrl: {safe_url}\n\nWebid: ```{webid}```\n\nWebshop: ```{webshop}```"
        url = f"https://api.telegram.org/{TELEGRAM_BOT}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=MarkDown"
        requests.post(url, timeout=10)

    def send_error_telegram(
        self, ticket_name: str, location: str
    ) -> None:
        """Sends a confirmation message to the telegram group"""
        text = f"❌ FansaleBot\n\nFailed Checkout\n{location}\n{ticket_name}"
        url = f"https://api.telegram.org/{TELEGRAM_BOT}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=MarkDown"
        requests.post(url, timeout=10)

    def start_checkout(self) -> list:
        """Starts the checkut threads"""
        fansale_url = self.target_offer.task.fansale_url
        eventim_url = self.target_offer.task.eventim_url
        event_id = self.target_offer.task.event_id

        while not self.captcha_bank.bank[fansale_url]:
            time.sleep(0.000001)
        while not self.captcha_bank.bank[eventim_url]:
            time.sleep(0.000001)
        while not self.eventim_bank.bank[event_id]:
            time.sleep(0.000001)
        while not self.cookie_bank.bank["cookies"]:
            time.sleep(0.000001)

        tokens = self.eventim_bank.get_token(event_id)
        fansale_cookies = self.cookie_bank.get_token("cookies")

        captchas_fansale = []
        for _ in range(len(self.captcha_bank.bank[fansale_url])):
            captchas_fansale.append(self.captcha_bank.get_token(fansale_url))

        captchas_eventim = []
        for _ in range(len(self.captcha_bank.bank[eventim_url])):
            captchas_eventim.append(self.captcha_bank.get_token(eventim_url))

        captchas = [captchas_fansale, captchas_eventim]
        return self.checkout_instance.flow(captchas, tokens, self.target_offer, fansale_cookies)

    def checkout_flow(self):
        self.print_cli(f"Checkout triggered for offer {self.target_offer.offer_id}", "yellow")
        redirect_url, cookies = self.start_checkout()
        if cookies:
            self.send_confirmation_telegram(
                redirect_url,
                cookies,
                self.target_offer.ticket_name,
                self.target_offer.task.location,
            )
            if self.ticket_blocking_mode:
                self.old_offer_ids = []
        else:
            self.send_error_telegram(
                self.target_offer.ticket_name,
                self.target_offer.task.location
            )

    def bedtime_state(self):
        self.captcha_bank.paused = True
        self.eventim_bank.paused = True
        while isNowInTimePeriod(datetime.time(23,30), datetime.time(6,15)):
            self.print_cli("Sleeping Mode Active (－_－) zzZ", "magenta")
            time.sleep(10)
        self.bedtime = False
        self.captcha_bank.paused = False
        self.eventim_bank.paused = False

    def run(self):
        """Main loop"""
        self.reset()
        while not self.target_offer_found:
            time.sleep(0.00001)
            if isNowInTimePeriod(datetime.time(23,30), datetime.time(6,15)):
                self.target_offer_found = True
                self.bedtime = True
        if self.target_offer_found and not self.bedtime:
            self.checkout_flow()
        elif self.bedtime:
            self.bedtime_state()
        
if __name__ == "__main__":
    controller = Controller()
    controller.setup()
    while True:
        controller.run()
