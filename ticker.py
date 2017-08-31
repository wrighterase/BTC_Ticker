#!/usr/bin/python

"Import needed libraries"
from dothat import backlight, lcd
from dot3k.menu import MenuOption, Menu
import json, requests
from time import sleep
import threading

"Clear the HAT screen and set static content"
lcd.clear(); lcd.set_contrast(50); backlight.set_graph(0)
lcd.set_cursor_position(0,0); lcd.write("Bittrex BTC-PAY:")

"bitstamp API url for updated price information"
"added bittrex prices for pairs"
#URL = 'https://www.bitstamp.net/api/ticker/'
URL = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-pay"
string = ""

class Ticker(MenuOption):
    def redraw(self,menu):
        menu.write_option(
            row=1,
            text=string,
            scroll=True
        )
        menu.clear_row(2)

menu = Menu(
    structure={
        'Bitcoin Ticker': Ticker()
    },
    lcd=lcd
)

menu.right()

"updates the price string from bitstamp every 5 seconds"
def update():
    while True:
        global string
        r = requests.get(URL)
        #priceFloat = float(json.loads(r.text)['last'])
	price = json.loads(r.text)['result'][0]['Last']
        string = "$" + str(price) + "/PAY"
        sleep(5)

"redraws the LCD screen with latest prices"
def scroller():
    x = 0
    while True:
	x +=3
	x %= 360
        backlight.sweep((360.0 - x) / 360.0)
        menu.redraw()
        sleep(0.01)

"start both loops at the same time"
if __name__ == '__main__':
    threading.Thread(target = update).start()
    threading.Thread(target = scroller).start()
