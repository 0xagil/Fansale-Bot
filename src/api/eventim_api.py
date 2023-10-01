import time
import requests
from src.utils.types import TargetOffer, Task

def init_checkout_session(
    task: Task
):
    """Initializes the checkout session"""
    burp0_url = f"{task.eventim_url}/api/cart/initialize/?affiliate={task.eventim_affiliate}&language=de&eventId={task.event_id}"
    burp0_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/addtocart-v1-initialize",
        "Origin": task.fansale_url,
        "Referer": task.fansale_url,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Te": "trailers",
    }
    response = requests.post(burp0_url, headers=burp0_headers, timeout=5)
    xsrf_token = response.json()["xsrfToken"]
    session_token = response.json()["sessionToken"]
    return xsrf_token, session_token

def add_cart(
    target_offer: TargetOffer,
    tokens: tuple,
    ticket_token: str,
    captcha: str,
):
    """Adds tickets to cart"""
    burp0_url = f"{target_offer.task.eventim_url}/api/cart/?affiliate={target_offer.task.eventim_affiliate}&token={tokens[0]}&gRecaptchaResponse={captcha}&evid={target_offer.task.event_id}"
    burp0_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/addtocart-v1-resale+json",
        "Origin": target_offer.task.fansale_url,
        "Referer": target_offer.task.fansale_url,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Te": "trailers",
    }
    burp0_json = {
        "backToPrevPage": f"{target_offer.task.fansale_url}/fansale/landingpage/taylorswift",
        "dataToken": ticket_token,
        "timestamp": int(round(time.time() * 1000)),
    }
    cookies = {
        "_abck": "",
        "bm_sz": ""
    }
    response = requests.put(
        burp0_url, headers=burp0_headers, json=burp0_json, cookies=cookies, timeout=5
    )
    redirect_url = response.json()["path"]
    cookies = response.cookies.get_dict()
    return redirect_url, cookies