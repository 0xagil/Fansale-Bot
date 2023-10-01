import time
import random
import src.api.fansale_api as fansale
import src.api.cookie_api as cookie
from src.mixins.cli import PrintableMixin
from src.utils.types import TargetOffer
from curl_cffi import requests as requests_ffi

class Monitor(PrintableMixin):
    """Class for monitoring the API for new tickets"""

    def __init__(self, proxies, task_list: list, identifier: int, Controller) -> None:
        self.task_list: list = task_list
        self.controller = Controller
        if self.controller.proxie_mode:
            self.proxies = proxies
        else:
            self.proxies = [{}]
        self.cookie_usage = 9
        self.cookies_inject = {}
        self.session = None
        super().__init__("Monitor", str(f"{identifier:02d}"))

    def parse_listings(self, raw_listings, category) -> list[tuple[str, list]]:
        """Parses the listings and returns a list of tuples with the offer id and the ticket ids"""
        matching_listings = []
        for offer in raw_listings:
            temp_tickets = [
                str(ticket["id"])
                for ticket in offer["tickets"]
                if any(x in ticket["locationInfo"] for x in category)
                and not ticket['sold']
            ]
            if temp_tickets:
                ticket_name = f"{offer['currentAmount']} Ticket: {offer['seatDescription']} - {offer['currentPrice']}$"
                matching_listings.append((str(offer["id"]), temp_tickets, ticket_name))
        return matching_listings

    def scrape_flow(self):
        """Scrapes the API for new tickets"""
        task_list = self.task_list.copy()
        random.shuffle(task_list)
        for task in task_list:
            if not self.controller.target_offer_found and task.active:
                if self.controller.cookie_injection_mode:
                    self.handle_cookies()
                if self.controller.proxie_mode:
                    proxy = random.choice(self.proxies)
                    self.proxy = {"https": "http://" + proxy}
                else:
                    self.proxy = {}
                t1 = time.time()
                status, raw_listings = fansale.get_event_offers(self.session, task, self.proxy, self.cookies_inject, self.browser_type)
                match status:
                    case 200:
                        matchings_listings = self.parse_listings(
                            raw_listings, task.category
                        )
                        matchings_listings = [
                            x
                            for x in matchings_listings
                            if x[0] not in self.controller.old_offer_ids
                        ]
                        if (
                            matchings_listings
                            and matchings_listings[0][0]
                            not in self.controller.old_offer_ids
                            and len(matchings_listings[0][1]) >= task.min_ticket
                        ):
                            self.print_cli(
                                f"Found {len(matchings_listings[0][1])} Ticket(s). OfferId: {matchings_listings[0][0]}",
                                "green",
                            )
                            offer = {
                                "offer_id": matchings_listings[0][0],
                                "tickets": matchings_listings[0][1],
                                "ticket_name": matchings_listings[0][2],
                                "task": task,
                            }
                            if not self.controller.target_offer_found:
                                self.controller.target_offer = TargetOffer(**offer)
                                self.controller.target_offer_found = True
                                self.controller.old_offer_ids.append(
                                    matchings_listings[0][0]
                                )
                        else:
                            self.print_cli(f"Speed: {round(time.time()-t1, 4)}s - No Tickets at E-ID: {task.event_id} - {task.location}", "white")
                            pass
                    case 418:
                        self.print_cli(f"Proxy Blocked {self.proxy}", "red")
                        self.cookie_usage = 10
                        pass
                    case 505:
                        self.print_cli("Connection Error", "red")
                        time.sleep(0.01)

    def handle_cookies(self):
        """Handles the cookie usage"""
        self.cookie_usage += 1
        if self.cookie_usage >= 8:
            self.session = requests_ffi.Session()
            browser_type = [
                "edge99",
                "edge101",
                "chrome110",
                "chrome107",
                "chrome104",
                "chrome101",
                "chrome100",
                "chrome99"
            ] 
            self.browser_type = random.choice(browser_type)
            self.cookie_usage = 0
            self.cookies_inject = cookie.get_cookie()
            while not self.cookies_inject:
                self.cookies_inject = cookie.get_cookie()
                time.sleep(1)

    def run(self):
        """Runs the monitors"""
        while True:
            self.scrape_flow()
            while self.controller.target_offer_found:
                time.sleep(0.1)
