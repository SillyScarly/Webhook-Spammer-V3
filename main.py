import os
import random
import sys
import threading
import time
from threading import Lock
from pyfiglet import Figlet

import requests
from colorama import Fore

os.system('cls')


def render(text, style):
    f = Figlet(font=style)
    print('\n' * 10)
    print(f.renderText(text))


render("Silly's Webhook Spammer", "banner3-D")

readym = input(f"{Fore.BLUE} This program will Webhook Spam as many webhooks as you desire with the help of proxies")

webhooks = open("webhooks.txt", "r").read().split("\n")

global myproxies
myproxies = open("proxy.txt", "r").read().split("\n")

os.system('cls & title SillyScarlys Webhook Spammer')

message = input(Fore.RED + "Message to Spam: ")
ratelimit = int(input("how many messages per second: "))
tospam = int(input("how many messages to spam: "))
hthreads = int(input("how many threads to use: "))

global newset
newset = set()


def control():
    global newset
    newstring = str(random.randint(1, 4000))
    newset.add(newstring)
    time.sleep(1.3)
    newset.remove(newstring)


global threadkill
threadkill = False

global msgsent
global msgfailed
msgfailed = 0
msgsent = 0


def spam(message):
    global newset
    global spammed
    global threadkill
    global myproxies
    global msgsent
    global msgfailed
    cc = 0
    while True:
        if threadkill:
            break
        if len(newset) >= ratelimit:
            time.sleep(0.1)
            continue
        web = random.choice(webhooks)
        try:
            https_proxy = str(random.choice(myproxies)).rstrip()
            if cc >= spammed:
                break

            try:
                proxies = {
                    "https": "https://" + https_proxy,
                }
                r = requests.post(web, json={"content": message}, proxies=proxies, timeout=10)
                s = [200, 201, 204]
                if r.status_code in s:
                    msgsent += 1
                    sys.stdout.write('\r' + Fore.GREEN + "Sent: " + str(msgsent) + " Failed: " + str(msgfailed))
                    cc += 1
                    threading.Thread(target=control).start()
                elif r.status_code == 429:
                    b = r.json()
                    msgfailed += 1
                    sys.stdout.write('\r' + Fore.GREEN + "Sent: " + str(msgsent) + " Failed: " + str(msgfailed))
                    time.sleep(2)
            except:
                proxies = {
                    "https": "http://" + https_proxy,
                }
                r = requests.post(web, json={"content": message}, proxies=proxies, timeout=10)
                s = [200, 201, 204]
                if r.status_code in s:
                    msgsent += 1
                    sys.stdout.write('\r' + Fore.GREEN + "Sent: " + str(msgsent) + " Failed: " + str(msgfailed))
                    cc += 1
                    threading.Thread(target=control).start()
                elif r.status_code == 429:
                    b = r.json()
                    msgfailed += 1
                    sys.stdout.write('\r' + Fore.GREEN + "Sent: " + str(msgsent) + " Failed: " + str(msgfailed))
                    time.sleep(0.1)


        except KeyboardInterrupt:
            threadkill = True
            break

        except:
            msgfailed += 1
            sys.stdout.write('\r' + Fore.GREEN + "Sent: " + str(msgsent) + " Failed: " + str(msgfailed))
            time.sleep(0.1)


def spamming():
    for i in range(hthreads):
        threading.Thread(target=spam, args=(message,)).start()


global spammed
spammed = tospam

lock = Lock()
spamming()

while True:
    try:
        time.sleep(0.00011)
    except KeyboardInterrupt:
        threadkill = True
        break
