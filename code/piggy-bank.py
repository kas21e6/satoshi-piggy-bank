import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import requests
import json
import threading
import argparse

parser = argparse.ArgumentParser(description="Satoshi Piggy Bank 🐷")

parser.add_argument(
    "--address",
    default="1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp",
    type=str,
    help="\
      This is the bitcoin address that the code will check for the satoshi balance.\
      Supports both segwit and legacy addresses\
    ",
)
parser.add_argument(
    "--fontsize",
    default=14,
    type=int,
    help="Determines how big the font on the screen is.",
)
parser.add_argument(
    "--lineheight",
    default=20,
    type=int,
    help="Determines how far the two lines are away from each other",
)
parser.add_argument(
    "--refreshrate",
    default=3600,
    type=int,
    help="This is how often the balance check will run. It's in seconds. 3600 is one hour.",
)

args = parser.parse_args()

BITCOIN_ADDRESS_TO_TRACK = args.address
FONT_SIZE = args.fontsize
LINE_HEIGHT = args.lineheight
REFRESH_RATE = args.refreshrate

i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

font = ImageFont.truetype(
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", FONT_SIZE
)


def format(number):
    return "{:,}".format(number)


def parseResponse(response):
    return json.loads(response.text)


def getSatoshiPrice():
    priceJsonResponse = parseResponse(
        requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    )
    return priceJsonResponse["bpi"]["USD"]["rate_float"] / 100000000


def getSatoshiBalance():
    response = requests.post(
        "https://www.blockonomics.co/api/balance",
        json={"addr": BITCOIN_ADDRESS_TO_TRACK},
    )
    parsedResponse = parseResponse(response)
    payload = parsedResponse["response"][0]
    return payload["confirmed"] + payload["unconfirmed"]


def getFormattedTotal(satoshiPrice, balance):
    total = satoshiPrice * balance
    roundedTotal = round(total, 2)
    return format(roundedTotal)


def getFormattedBalance(balance):
    return format(balance)


def printScreen():
    threading.Timer(REFRESH_RATE, printScreen).start()

    satoshiPrice = getSatoshiPrice()
    balance = getSatoshiBalance()

    formattedTotal = getFormattedTotal(satoshiPrice, balance)
    formattedBalance = getFormattedBalance(balance)

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), "@: " + formattedBalance, font=font, fill=105)
    draw.text((0, LINE_HEIGHT), "$: " + formattedTotal, font=font, fill=105)

    disp.image(image)
    disp.show()


printScreen()
