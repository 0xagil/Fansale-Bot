from src.utils.types import Task, CaptchaSite

BANNER = """

          █████▒▄▄▄       ███▄    █   ██████  ▄▄▄       ██▓    ▓█████     ▄▄▄▄    ▒█████  ▄▄▄█████▓
        ▓██   ▒▒████▄     ██ ▀█   █ ▒██    ▒ ▒████▄    ▓██▒    ▓█   ▀    ▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
        ▒████ ░▒██  ▀█▄  ▓██  ▀█ ██▒░ ▓██▄   ▒██  ▀█▄  ▒██░    ▒███      ▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
        ░▓█▒  ░░██▄▄▄▄██ ▓██▒  ▐▌██▒  ▒   ██▒░██▄▄▄▄██ ▒██░    ▒▓█  ▄    ▒██░█▀  ▒██   ██░░ ▓██▓ ░ 
        ░▒█░    ▓█   ▓██▒▒██░   ▓██░▒██████▒▒ ▓█   ▓██▒░██████▒░▒████▒   ░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ 
        ▒ ░    ▒▒   ▓▒█░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░ ▒▒   ▓▒█░░ ▒░▓  ░░░ ▒░ ░   ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   
        ░       ▒   ▒▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░  ▒   ▒▒ ░░ ░ ▒  ░ ░ ░  ░   ▒░▒   ░   ░ ▒ ▒░     ░    
        ░ ░     ░   ▒      ░   ░ ░ ░  ░  ░    ░   ▒     ░ ░      ░       ░    ░ ░ ░ ░ ▒    ░      
                    ░  ░         ░       ░        ░  ░    ░  ░   ░  ░    ░          ░ ░     f*** eventim
                    ░                                                                       f*** akamai
                                                                                by 0xagil
        """

print(BANNER)

TELEGRAM_BOT = " "
CHAT_ID = " "
CAPSOLVER_KEY = " "
THREAD_AMOUNT = 100

assert TELEGRAM_BOT != " ", "Please enter your telegram bot token in settings.py"
assert CHAT_ID != " ", "Please enter your telegram chat id in settings.py"
assert CAPSOLVER_KEY != " ", "Please enter your capsolver key in settings.py"

CAPTCHA_SITES = [
    CaptchaSite(
        url="https://www.fansale.de",
        site_key="6LcOq0IUAAAAAKm8wo7r4s4Uf5DrcVlyoxclRNQF",
        delay=50,
    ),
    CaptchaSite(
        url="https://www.eventim.de",
        site_key="6LdiRiUUAAAAAMiTg8Kc4LVRkF3p1zPfzzi6I-e_",
        delay=50,
    ),
]

TASK_LIST = [
    Task(
        event_id="17348350",
        category=["Stehplatz", "Innenraum", " "],
        min_ticket=1,
        fansale_url="https://www.fansale.de",
        eventim_url="https://www.eventim.de",
        eventim_affiliate="WCO",
        active=True,
        location="GELSENKIRCHEN, Mittwoch",
    ),
    Task(
        event_id="17229936",
        category=["Stehplatz", "Innenraum", " "],
        min_ticket=1,
        fansale_url="https://www.fansale.de",
        eventim_url="https://www.eventim.de",
        eventim_affiliate="WCO",
        active=True,
        location="GELSENKIRCHEN, Donnerstag",
    ),
    Task(
        event_id="17348408",
        category=["Stehplatz", "Innenraum", " "],
        min_ticket=1,
        fansale_url="https://www.fansale.de",
        eventim_url="https://www.eventim.de",
        eventim_affiliate="WCO",
        active=True,
        location="GELSENKIRCHEN, Freitag",
    ),
    Task(
        event_id="17348446",
        category=["Stehplatz", "Innenraum", "FOS", "17A", "18A", " "],
        min_ticket=1,
        fansale_url="https://www.fansale.de",
        eventim_url="https://www.eventim.de",
        eventim_affiliate="WCO",
        active=True,
        location="HAMBURG, Mittwoch",
    ),
    Task(
        event_id="17318939",
        category=["Stehplatz", "Innenraum", "FOS", "17A", "18A", " "],
        min_ticket=1,
        fansale_url="https://www.fansale.de",
        eventim_url="https://www.eventim.de",
        eventim_affiliate="WCO",
        active=True,
        location="HAMBURG, Dienstag",
    ),
    Task(
        event_id="17333071",
        category=[" ", "Innenraum", "Z2", "Z1", "Z3", "Z4", " ", "FOS"],
        min_ticket=1,
        fansale_url="https://www.fansale.de",
        eventim_url="https://www.eventim.de",
        eventim_affiliate="WCO",
        active=True,
        location="MÜNCHEN, Samstag",
    ),
    Task(
        event_id="17348667",
        category=[" ", "Innenraum", "Z2", "Z1", "Z3", "Z4", " ", "FOS"],
        min_ticket=1,
        fansale_url="https://www.fansale.de",
        eventim_url="https://www.eventim.de",
        eventim_affiliate="WCO",
        active=True,
        location="MÜNCHEN, Sonntag",
    ),
    Task(
        event_id="17337852",
        category=["Left", "Right", "GA", "Standing"],
        min_ticket=1,
        fansale_url="https://www.fansale.at",
        eventim_url="https://www.oeticket.com",
        eventim_affiliate="FS6",
        active=False,
        location="WIEN, Samstag",
    ),
    Task(
        event_id="17275983",
        category=["Left", "Right", "GA", "Standing"],
        min_ticket=1,
        fansale_url="https://www.fansale.at",
        eventim_url="https://www.oeticket.com",
        eventim_affiliate="FS6",
        active=False,
        location="WIEN, Freitag",
    ),
    Task(
        event_id="17337851",
        category=["Left", "Right", "GA", "Standing"],
        min_ticket=1,
        fansale_url="https://www.fansale.at",
        eventim_url="https://www.oeticket.com",
        eventim_affiliate="FS6",
        active=False,
        location="WIEN, Donnerstag",
    ),
]
