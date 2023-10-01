import src.api.fansale_api as fansale
import src.api.eventim_api as eventim
from src.mixins.cli import PrintableMixin
from multiprocessing.pool import ThreadPool
import time

class Checkout(PrintableMixin):
    """Class for checking out tickets"""
    __slots_ = ('captchas', 'tokens', 'target_offer')
    def __init__(
        self
    ) -> None:

        super().__init__("Checkout Instance", "")

        self.print_cli(f"Initiated Checkout Instance", "green")

    def checkout_flow(self, target_offer, captcha_fansale, captcha_eventim, cookies_fansale, tokens, i):
        appendix = f"Thread {i} -"
        self.print_cli(f"{appendix} Started checkout process", "white")
        state, ticket_token, error = fansale.reserve_tickets(
            target_offer, captcha_fansale, cookies_fansale
        )
        if ticket_token:
            self.print_cli(f"{appendix} Received Checkout token", "yellow")
            redirect_url, cookies = eventim.add_cart(
                target_offer,
                tokens,
                ticket_token,
                captcha_eventim
            )
            if not "errorcode" in redirect_url:
                self.print_cli(f"{appendix} Ticket added to cart", "green")
            return redirect_url, cookies
        else:
            self.print_cli(f"{error}", "red")
            return "errorcode", {}

    def flow(self, captchas: list, tokens: tuple, target_offer: dict, cookies_fansale: dict):
        """Checks out tickets"""
        captchas_fansale = captchas[0]
        captchas_eventim = captchas[1]

        self.print_cli("Reserving tickets..", "yellow")

        amount = (
            len(captchas_eventim)
            if len(captchas_eventim)
            < len(captchas_fansale)
            else len(captchas_fansale)
        )
        for i in range(amount):
            captcha_fansale = captchas_fansale[i]
            captcha_eventim = captchas_eventim[i]
            redirect_url, cookies = self.checkout_flow(target_offer, captcha_fansale, captcha_eventim, cookies_fansale, tokens, i+1)
            if not "errorcode" in redirect_url:
                self.print_cli("Sending cookies to main thread", "green")
                return redirect_url, cookies
        self.print_cli("Failed to add to cart", "red")
        return "", {}