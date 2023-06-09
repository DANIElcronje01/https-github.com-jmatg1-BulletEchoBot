import os
import time
from datetime import datetime
from PIL import Image
from tkinter import Tk, Button, Text, END
from tkinter import ttk
import re

import threading
from subprocess import check_output

tkWindow = Tk()
tkWindow.geometry('400x250')
tkWindow.title('Bullet ECho Bot v 4.3.1 By Jmatg1')

class Bot:
    work = 1
    screenshot = 0
    t1 = 0
    fight = 1
    device = 0
    controlsUnderBuilding = [(576, 431), (1059, 768)]
    # def __init__(self):
    def shadeVariation(self, col, col2, shade = 0):
        if shade == 0:
            return col == col2
        rezult = (abs(col[0] - col2[0]), abs(col[1] - col2[1]), abs(col[2] - col2[2]))
        shadowCount = 0
        for rgb in rezult:
            if rgb <= shade:
                shadowCount += 1
        return shadowCount == 3

    def getXYByColor(self, color, isGetSCreen=True, shade = 0, startXY = (0,0), endXY=(0,0)):
        if (isGetSCreen):
            self.getScreen()
        img = self.screenshot
        coordinates = False


        if endXY[0] == 0 and endXY[1] == 0:
            endXY = (img.size[0], img.size[1])
        for x in range(img.size[0]):
            if not(startXY[0] < x < endXY[0]):
                continue

            for y in range(img.size[1]):
                if not(startXY[1] < y < endXY[1]):
                    continue
                if self.shadeVariation(img.getpixel((x, y))[:3],  color, shade):
                    coordinates = (x, y)
                    continue
        return coordinates

    def pixelSearch(self, x1, y1, color):  # x2=1600, y2=900,
        # im = ImageOps.crop(im, (x1, y1, x2, y2))
        colorPixel = self.screenshot.getpixel((x1, y1))[:3]
        if colorPixel == color:
            return True
        else:
            return False

    def getScreen(self):
        self.shell(f'/system/bin/screencap -p /sdcard/{self.device}-screenshot.png')
        # os.system('hd-adb shell /system/bin/screencap -p /sdcard/screenshot.png')
        # Using the adb command to upload the screenshot of the mobile phone to the current directory

        os.system(f'hd-adb -s {self.device} pull /sdcard/{self.device}-screenshot.png')
        try:
            self.screenshot = Image.open(f"{self.device}-screenshot.png")
        except ValueError:
            print(ValueError)
            self.getScreen()

    def getPixelColor(self, x1, y1):
        self.getScreen()
        im = Image.open(f"{self.device}-screenshot.png")
        # im1 = ImageOps.crop(im, (0, 0, 1000, 300))
        # im1.show()
        pixelRGB = im.getpixel((x1, y1))[:3]
        return pixelRGB

    def click(self, x, y, timer=True):
        if (timer):
            time.sleep(1)
        # os.system(f'hd-adb shell input tap {x} {y}')
        self.shell(f'input tap {x} {y}')
        if (timer):
            time.sleep(1)

    def main(self):
        while self.work:
            # self.log('Get ScreenShot')
            self.getScreen()

            # self.log('Scan')

            self.skipAds()

            if self.isMainScreen():
                self.log('Main Screen')
                self.collectBoxBot()
                if self.isEventActive():
                    self.log('isEventActive')
                    self.openEvent()
                    self.eventBot()
                elif self.isMissionsActive():
                    self.click(120, 555)
                    self.collectContract()
                    self.clickBack()
                else:
                    self.clickPlay()
                continue

            if self.isEventScreen():
                self.log('Event Screen')
                self.eventBot()
                continue

            if self.isFightScreen():
                self.log('Fight Screen')
                self.click(1280, 450) # 1 skill
                self.keyW(10000)
                self.click(1480, 335) # 2 skill
                continue

            if self.isCollectScreen():
                self.log('Collect Screen')
                self.click(611, 669) # Skip Series
                self.click(803, 769) # Collect
                self.getScreen()
                continue

            if self.isTableRezultScreen():
                self.log('Table Screen')
                self.click(803, 769) # Next
                self.getScreen()
                continue

            if self.isFriendsScreen():
                self.log('Friends Screen') # enothe
                continue

            if self.isMissionsScreen():
                self.log('Missions Screen')
                self.missionBot()
                self.clickBack()
                continue

            if self.isHeroesScreen():
                self.log('Heroes Screen')
                self.click(67, 50)
                continue

            if self.isShopScreen():
                self.log('Shop Screen')
                self.click(67, 50)
                continue



    def skipAds(self):
        if self.pixelSearch(926, 770, (110, 204, 22)): # Skip league
            self.log('Skip league')
            self.click(926, 770)
            time.sleep(3)
            self.keyBack()
        if self.pixelSearch(566, 560, (238, 72, 35)): # Повышение level1
            self.log('Повышение level 1')
            self.click(566, 560)
        if self.pixelSearch(446, 166, (47, 77, 129)): # Повышение level2
            self.log('Повышение level 2')
            self.click(1034, 782)
        if self.pixelSearch(446, 166, (251, 164, 20)): # Повышение рейтинга
            self.log('Повышение рейтинга')
            self.clickBack()
        if self.pixelSearch(530, 290, (17, 115, 202)): # Autokick
            self.log('Autockic detected')
            self.keyBack()
        if self.pixelSearch(530, 290, (17, 114, 201)): # Autokick
            self.log('Autockic detected')
            self.keyBack()
        if self.pixelSearch(873, 791, (155, 23, 224)): # Contract
            self.log('Contracts detected')
            self.keyBack()
        if self.pixelSearch(446, 166, (82, 58, 215)): # Братья по оружию
            self.log('Братья по оружию')
            closeIcon = self.getXYByColor((62, 29, 171), True, 0, (854, 123), (1583, 251))
            if closeIcon:
                self.log('closeIcon')
                self.click(closeIcon[0], closeIcon[1])
            redBtn = self.getXYByColor((236, 69, 32), True, 3, (573, 498), (1222, 664))
            if redBtn:
                self.click(redBtn[0], redBtn[1])
                time.sleep(1)

        closeIcon = self.getXYByColor((4, 66, 148), True, 0, (137, 160), (1594, 251))
        if closeIcon:
            self.log('closeIcon')
            self.click(closeIcon[0], closeIcon[1])
            redBtn = self.getXYByColor((236, 69, 32), True, 0, (573, 498), (1222, 664))
            if redBtn:
                self.click(redBtn[0], redBtn[1])
                time.sleep(1)

    def isMainScreen(self):
        btnPlay = self.getXYByColor((25, 52, 135), True, 0, (1345, 35), (1583, 251))
        if btnPlay:
            return True
        else:
            return False

    def isEventScreen(self):
        if self.pixelSearch(1345, 35, (8, 8, 19)):
            return True
        else:
            return False

    def isEventActive(self):
        x1 = 196
        y1 = 306
        # self.getPixelColor(x1, y1)
        if self.pixelSearch(x1, y1, (255, 210, 31)):
            return True
        else:
            return False

    def isMissionsActive(self):
        x1 = 196
        y1 = 514
        # self.log(self.getPixelColor(x1, y1))
        if self.pixelSearch(x1, y1, (255, 210, 31)):
            return True
        else:
            return False

    def isReadyBox(self):
        x1 = 251
        y1 = 831
        if self.pixelSearch(x1, y1, (254, 172, 39)):
            return True
        else:
            return False

    def eventBot(self):
        self.missionBot()
        self.clickPlay()
        time.sleep(1)
        if self.isTicketsOver():
            self.log('Tickets is Over')
            self.click(1060, 275)
            self.click(67, 50)

    def collectContract(self):
        self.log('Start collectContract Bot')

        self.log('3h contract')
        self.click(280, 180)
        self.missionBot()

        self.log('8h contract')
        self.click(280, 280)
        self.missionBot()

        self.log('21h contract')
        self.click(280, 380)
        self.missionBot()

        self.log('2d contract')
        self.click(280, 480)
        self.missionBot()

        self.log('1w contract')
        self.click(280, 580)
        self.missionBot()

        self.log('END collectContract Bot')
         
    def collectBoxBot(self):
        self.log('Start collectBoxBot')
        hasMission = True
        while hasMission:
            self.getScreen()
            cord = self.getXYByColor((254, 171, 39), True, 0, (212, 708), (630, 900))
            if cord:
                self.log('Collect Box')
                self.click(cord[0], cord[1])
                time.sleep(1)
                self.keyBack()
            else:
                hasMission = False
        self.log('END collectBoxBot')

    def missionBot(self):
        self.log('Start Mission Bot')
        hasMission = True
        while hasMission:
            self.getScreen()
            cord = self.getXYByColor((254, 171, 39), True, 0, (413, 407),(1200, 800))
            if cord:
                self.log('Collect Box')
                self.click(cord[0], cord[1])
                time.sleep(1)
                self.keyBack()
            else:
                hasMission = False
        self.log('END Mission Bot')

    def isTicketsOver(self):
        self.getScreen()
        x1 = 515
        y1 = 290
        # self.getPixelColor(x1, y1)
        if self.pixelSearch(x1, y1, (17, 113, 201)):
            return True
        else:
            return False

    def isCollectScreen(self):
        if self.pixelSearch(680, 780, (106, 202, 18)):  # 1340, 30, 1350, 40,
            return True
        else:
            return False

    def isTableRezultScreen(self):
        x1 = 380
        y1 = 105
        # self.getPixelColor(x1, y1)
        if self.pixelSearch(x1, y1, (0, 55, 112)):
            return True
        else:
            return False

    def isFightScreen(self):
        if self.pixelSearch(230, 45, (156, 201, 228)):  # 1340, 30, 1350, 40,
            return True
        else:
            return False

    def isFriendsScreen(self):
        if self.pixelSearch(1345, 35, (9, 19, 35)):
            return True
        else:
            return False

    def isMissionsScreen(self):
        x1 = 570
        y1 = 120
        # self.getPixelColor(x1, y1)
        if self.pixelSearch(x1, y1, (18, 150, 234)):
            return True
        else:
            return False

    def isHeroesScreen(self):
        x1 = 275
        y1 = 417
        # self.getPixelColor(x1, y1)
        if self.pixelSearch(x1, y1, (187, 104, 24)): # кулачек
            return True
        else:
            return False

    def isShopScreen(self):
        x1 = 930
        y1 = 840
        # self.getPixelColor(x1, y1)
        if self.pixelSearch(x1, y1, (1, 88, 153)):
            return True
        else:
            return False

    def openEvent(self):
        self.click(120, 337)

    def clickPlay(self):
        self.click(1366, 866)

    def clickBack(self):
        self.click(67, 50)

    def keyW(self, ms):
        self.shell(f'input swipe 250 700 250 600 {ms}')

    def keyQ(self):
        self.shell(f'input keyevent 45')

    def keyE(self):
        self.shell(f'input keyevent 33')

    def keyBack(self):
        self.shell(f'input keyevent 4')

    def start(self):
        self.device = inputDevice.get()
        self.work = 1
        self.t1 = threading.Thread(target=self.main, args=[])
        self.t1.start()

    def stop(self):
        self.work = 0

    def closeWindow(self):
        self.work = 0
        tkWindow.destroy()

    def shell(self, cmd):
        os.system(f'hd-adb -s {self.device} shell {cmd}')

    def log(self, value):
        timeVal = datetime.now().strftime("%D %H:%M:%S")
        logString = "%s %s" % (timeVal, value)
        text.insert(END, logString + " \r\n")
        text.see("end")
        f = open("log.txt", "a")
        f.write(logString + " \r")
        f.close()

    def selectedDevice(self, event):
        self.device = inputDevice.get()

bot = Bot()
buttonStart = Button(tkWindow, text='Start', command=bot.start)
buttonStart.pack()
buttonStop = Button(tkWindow, text='Stop', command=bot.stop)
buttonStop.pack()

tkWindow.protocol("WM_DELETE_WINDOW", bot.closeWindow)
devList = check_output("hd-adb devices")
text = Text(tkWindow, height=10, width=50)
text.insert(END, devList)



print(devList)
devListArr = re.compile(r'emulator-\d\d\d\d').findall(str(devList))
print('ARRAY DEVICES', devListArr)
rezArr = []
for x in devListArr:
    if (x.startswith('emulator-')):
        rezArr.append(x)
print(rezArr)

inputDevice = ttk.Combobox(tkWindow, width=15)
inputDevice['values'] = rezArr
inputDevice.bind("<<ComboboxSelected>>", bot.selectedDevice)
inputDevice.current(0)
inputDevice.pack()
text.pack()

tkWindow.mainloop()
