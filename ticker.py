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
last = 0

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

"""
updates the price string from bitstamp every 5 seconds
sets the HAT LED graph when price changes.
LED 0 is on if up.  LED 5 is on if down
"""

def update():
    while True:
        global string, last
        r = requests.get(URL, verify=False)
        #uncomment to use bitstamp api
        #priceFloat = float(json.loads(r.text)['Last'])
        price = float(json.loads(r.text)['result'][0]['Last'])
        if price > last:
            backlight.graph_set_led_state(0,1)
            backlight.graph_set_led_state(5,0)
            last = price
        elif price < last:
            backlight.graph_set_led_state(0,0)
            backlight.graph_set_led_state(5,1)
            last = price
        string = "$" + str(price)
        sleep(0.5)

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
