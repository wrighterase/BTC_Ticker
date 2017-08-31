#!/usr/bin/python
from dothat import backlight, lcd
from dot3k.menu import MenuOption, Menu
import json, requests
from time import sleep
import threading

lcd.clear(); lcd.set_contrast(50); backlight.set_graph(0)
backlight.rgb(0,255,0)
lcd.set_cursor_position(0,0); lcd.write("Bitstamp:")
URL = 'https://www.bitstamp.net/api/ticker/'
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

def update():
    while True:
        global string
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['last'])
        #return priceFloat
        #print "Bitstamp last price: $" + str(priceFloat) + "/BTC"
        #lcd.set_cursor_position(0,2); lcd.write("$" + str(ticker()) + "/BTC")
        string = "$" + str(priceFloat) + "/BTC"
        sleep(5)

def scroller():
    while True:
        menu.redraw()
        sleep(0.01)

if __name__ == '__main__':
    threading.Thread(target = update).start()
    threading.Thread(target = scroller).start()
