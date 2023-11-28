<!-- PROJECT LOGO -->
<br />
    <h3 align="center"> Automated Ticket Buying on Fansale and Eventim </h3>
    <h4 align="center"> Currently this solution will be too slow! </h3>
</div>

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
## Getting Started

Purchase your preferred tickets effortlessly through Fansale and Eventim automatically.
To get a local copy up and running follow these simple example steps:

## Disclaimer
* Only buy the Tickets for yourself.
* Do not resell those tickets on platforms like eBay or Viagogo.
* Please research the legal status of reselling tickets in your country.
* This porgram is for educational purpose only!
* Do not DDOS their website with too many requests.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Python
  ```sh
  sudo apt-get -y install python3
  ```
* Pip
  ```sh
  sudo apt-get -y install python3-pip
  ```
* Cookie Farming API for bypassing AKAMAI
  ```sh
  atm valid cookies are obtained from any other challenge url except the target ticket site since their latest bot protection update
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/0xagil/Fansale-Bot.git
   ```
2. Install pip packages
   ```sh
   pip install -r requirements.txt
   ```
3. Start the Program to Monitor the Tickets
   ```sh
   python3 bot_v3.py
   ```

<!-- USAGE EXAMPLES -->
## Usage

1. Modify the settings and the Events which are needed to be monitored
2. Sit back and wait until the program reserves a ticket and copy the cookies into the browser
3. Buy your Ticket

## Update
- Currently Supports multiple pages (DE, AT)

<!-- ROADMAP -->
## Roadmap

- [X] Run the Program on a VPS
- [X] Send Notifications on Telegram
- [X] Design the Programm so the tickets can be bought mobile (Telegram)
