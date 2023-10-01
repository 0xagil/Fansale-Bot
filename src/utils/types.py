from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    """Class for storing task information."""
    event_id: str
    category: list
    min_ticket: int
    fansale_url: str
    eventim_url: str
    eventim_affiliate: str
    active: bool
    location: str

@dataclass
class CaptchaSite:
    """Class for storing captcha site information."""
    url: str
    site_key: str
    delay: int

@dataclass
class TargetOffer:
    """Class for storing target offer information."""
    offer_id: str
    tickets: list
    ticket_name: str
    task: Task
