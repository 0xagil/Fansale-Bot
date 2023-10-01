import time
import random
from collections import OrderedDict
from src.utils.types import TargetOffer
from curl_cffi import requests as requests_ffi
import json

def get_event_offers(session, task, proxies: dict, cookies_inject: dict, browser_type: str):
    """Gets the current offers for a specific event"""
    url = f"https://www.fansale.de/fansale/json/offers/{task.event_id}"
    headers = OrderedDict({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Sec-Ch-Ua": '"Chromium";v="116", "Not/A)Brand";v="8"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    })
    try:
        response = session.get(url, headers=headers, cookies=cookies_inject, proxies=proxies, timeout=3, impersonate=browser_type)
        if "Access Denied" in response.text:
            return 418, []
        return 200, response.json()["offers"]
    except Exception as e:
        return 505, []
    
def reserve_tickets(target_offer: TargetOffer, recaptcha: str, cookies=dict):
    """Reserves tickets for a specific offer"""
    tickets_string = "&tickets=".join(target_offer.tickets)
    burp0_url = f"{target_offer.task.fansale_url}/fansale/offerView/{target_offer.offer_id}/checkBarcode.htm?tickets={tickets_string}&g-recaptcha-response={recaptcha}&_={int(round(time.time()*1000))}"
    headers = OrderedDict({
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Referer": f"{target_offer.task.fansale_url}/fansale/tickets/rock-pop/taylor-swift/448410",
        "Sec-Ch-Ua": '"Chromium";v="116", "Not/A)Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        "X-Requested-With": "XMLHttpRequest",
    })
    response = requests_ffi.get(burp0_url, headers=headers, cookies=cookies, timeout=4, impersonate='edge101')
    state = response.json()["valid"]
    ticket_token = response.json()["token"]
    error = response.json()["errorMessage"]
    return state, ticket_token, error
