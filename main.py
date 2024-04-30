import pygame
import math
import random
import platform
if platform.system() == "Windows":
    import win32gui
    import win32con

##AI FUNCTIONS

name = "2048 AI Version"
resX = 800
resY = 600
background = (50, 50, 50); 

btnActivated = (226,240,247)
btnActivated = (240,256,256)
btnDisactivated = (126, 140, 147)
primary = (100, 100, 100)

colorList = [background,
             (128, 0, 0),
             (154, 99, 36),
             (128, 128, 0),
             (70, 153, 144),
             (0, 0, 117),
             (0, 0, 0),
             (230, 25, 75),
             (245, 130, 49),
             (255, 225, 25),
             (191, 239, 69),
             (60, 180, 75),
             (66, 212, 244),
             (67, 99, 216),
             (67, 99, 216)]
tColorList = [(0,0,0),
              (255,255,255),
              (255,255,255),
              (255,255,255),
              (255,255,255),
              (255,255,255),
              (255,255,255),
              (255,255,255),
              (255,255,255),
              (255,255,255),
              (255,255,255),
              (255,255,255)]


##Game Settings
startX = 10
startY = 50
sizeBox = 160
spaceBox = 2
numBoxesX = 4
numBoxesY = 4
waterfall = False
advancedRandom = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

## Important Variables
endOfGameX = startX + numBoxesX * (spaceBox + sizeBox)
endOfGameY = startY + numBoxesY * (spaceBox + sizeBox)
maxScore = 0
bottomOfHeader = startY
fullscreen = False
ai = False
victory = False
loopBack = False

## Create Array
maxScore = 1
arr = [0]
for i in range(numBoxesX-1):
    arr.append(0)
valList = [arr]
for i in range(numBoxesY-1):
    arr = [0]
    for i in range(numBoxesX-1):
        arr.append(0)
    valList.append(arr)

## -------- DISPLAY FUNCTIONS -------- 

##Initialize Pygame
pygame.init()
gameDisplay = pygame.display.set_mode((resX,resY), pygame.RESIZABLE)
if platform.system() == "Windows":
   window = win32gui.GetForegroundWindow()
pygame.display.set_caption(name)
font = pygame.font.Font('freesansbold.ttf', 15)
font2 = pygame.font.Font('freesansbold.ttf', int(sizeBox/2-5))

clock = pygame.time.Clock()

def initPyGame():
    pygame.init()
    global gameDisplay, endOfGameX, endOfGameY, font, font2, clock
    endOfGameX = startX + numBoxesX * (spaceBox + sizeBox)
    endOfGameY = startY + numBoxesY * (spaceBox + sizeBox)
    resizeDisplay()
    pygame.display.set_caption(name)
    font = pygame.font.Font('freesansbold.ttf', 15)
    font2 = pygame.font.Font('freesansbold.ttf', int(sizeBox/2-5))
    clock = pygame.time.Clock()
    initDisplay()

def resizeDisplay():
    if not fullscreen:
        global endOfGameX, endOfGameY, resX, resY
        endOfGameX = startX + numBoxesX * (spaceBox + sizeBox)
        endOfGameY = startY + numBoxesY * (spaceBox + sizeBox)
        resX = endOfGameX + 10
        resY = endOfGameY + 10
        pygame.display.set_mode((resX,resY),pygame.RESIZABLE)

crashed = False
def initDisplay():
    ## Header
    if platform.system() == "Windows":
        global window
        win32gui.ShowWindow(window, win32con.SW_SHOWNOACTIVATE)
        win32gui.BringWindowToTop(window)
    gameDisplay.fill(background)
    pygame.draw.rect(gameDisplay,primary,pygame.Rect(10,10,resX - 20, 30), border_radius=10)
    text = font.render(name, True, background, primary)
    textRect = text.get_rect()
    pygame.draw.rect(gameDisplay,background,pygame.Rect(startX,startY,endOfGameX-startX, endOfGameY-startY), border_radius=10)
 
    textRect.center = (resX // 2, 25)
    gameDisplay.blit(text, textRect)
    renderGame()

def drawBox(num,x,y):
    spacing = sizeBox + spaceBox
    colNum = num % 12
    color = colorList[colNum]
    pygame.draw.rect(gameDisplay,color,pygame.Rect(startX+x*spacing,startY+y*spacing,sizeBox,sizeBox),border_radius=round(sizeBox/16))
    if num > 0 and sizeBox > 40:
        text = font2.render(str(round(math.pow(2,num))), True, tColorList[colNum])
        textRect = text.get_rect()
        textRect.center = (startX+x*spacing+sizeBox/2, startY+y*spacing+sizeBox/2)
        gameDisplay.blit(text, textRect)


def renderGame():
    spacing = sizeBox + spaceBox
    ## Draw Background Rectangles
    for x in range(numBoxesX):
        for y in range(numBoxesY):
            drawBox(valList[y][x],x,y)

## ------------ OTHER FUNCTIONS ------------

def restartGame():
    global valList
    arr = [0]
    for i in range(numBoxesX-1):
        arr.append(0)
    valList = [arr]
    for i in range(numBoxesY-1):
        arr = [0]
        for i in range(numBoxesX-1):
            arr.append(0)
        valList.append(arr)
    victory = False
    genFirst()
    renderGame()



def expandArray():
    global valList
    while numBoxesY > len(valList):
        arr = [0]
        for i in range(numBoxesX-1):
            arr.append(0)
        valList.append(arr)
    deficitX = numBoxesX - len(valList[0])
    if deficitX:
        for y in range(numBoxesY):
            for i in range(deficitX):
                valList[y].append(0)

def settingConfig():
    quitSet = False
    noPress = False
    pygame.display.iconify()
    global sizeBox, numBoxesX, numBoxesY, advancedRandom, waterfall, loopBack, startX, startY
    print(bcolors.HEADER + "Please select the setting you'd like to change: ") 
    print(bcolors.OKBLUE + " 1 - Box Size ") 
    print(bcolors.OKBLUE + " 2 - # of Columns ") 
    print(bcolors.OKBLUE + " 3 - # of Rows")
    print(bcolors.OKBLUE + " 4 - Max Out Display")  
    print(bcolors.OKBLUE + " 5 - Advanced Random ") 
    print(bcolors.OKBLUE + " 6 - Waterfall Simulator ") 
    print(bcolors.OKBLUE + " 7 - Loop Back Mode ") 
    print() 
    print(bcolors.OKBLUE + " A - AI Gesture Mode (Erases Data)") 
    print() 
    print(bcolors.OKGREEN + " H - Help ") 
    print(bcolors.WARNING + " R - Reset to Defaults")
    print(bcolors.FAIL + " Q - Quit and Save")
    while not quitSet:
        c = input(bcolors.OKCYAN + "\nPlease enter a command: ")
        if c == "1":
            global font2
            inputStr = input("What would you like to change the box size to? (Default: 80): ")
            if inputStr.isdigit():
                sizeBox = int(inputStr)
            else:
                print(bcolors.WARNING + "Keeping Current Values")
            font2 = pygame.font.Font('freesansbold.ttf', int(sizeBox/2-5))
        elif c == "2":
            inputStr = input("What would you like to change the # of Columns too? (Defualt: 4) ")
            if inputStr.isdigit():
                numBoxesX = int(inputStr)
            else:
                print(bcolors.WARNING + "Keeping Current Values")
            expandArray()
        elif c == "3":
            inputStr = input("What would you like to change the # of Rows too? (Defualt: 4): ")
            if inputStr.isdigit():
                numBoxesY = int(inputStr)
            else:
                print(bcolors.WARNING + "Keeping Current Values")
            expandArray()
        elif c == "4":
            inputStr = input("What is your monitor's Width?: ")
            if inputStr.isdigit():
                numBoxesX = math.floor((int(inputStr) - (startX)) / (sizeBox + spaceBox))
            else:
                print(bcolors.WARNING + "Keeping Current Values for width")
            expandArray()
            inputStr = input("What is your monitor's Height?: ")
            if inputStr.isdigit():
                numBoxesY = math.floor((int(inputStr) - (startY)) / (sizeBox + spaceBox))
                print("Your Display is (", numBoxesX, ",", numBoxesY, ") Boxes")
            else:
                print(bcolors.WARNING + "Keeping Current Values for height")
            expandArray()
        elif c == "5":
            val = input("Would you like to use advanced random? It allows you to get more than just 2's and 4's. \n(Current Value is: " + str(advancedRandom) + ", default is: False) [y/n] ")
            if val.lower() == "y":
                advancedRandom = True
            elif val.lower() == "n":
                advancedRandom = False
            else:
                print(bcolors.WARNING + "Keeping Current Values")
        elif c == "6":
            val = input("Would you like to use waterfall mode? This mode causes the computer to automatically press down as fast as possible to create a waterfall effect. \n(Current Value is: " + str(waterfall) + ", default is: False) [y/n] ")
            if val.lower() == "y":
                waterfall = True
            elif val.lower() == "n":
                waterfall = False
            else:
                print("Keeping Current Values")
        elif c == "7":
            val = input("Would you like to use loop back mode? This mode causes the board to loop around, defeating the corner strategy \n(Current Value is: " + str(loopBack) + ", default is: False) [y/n] ")
            if val.lower() == "y":
                loopBack = True
            elif val.lower() == "n":
                loopBack = False
            else:
                print(bcolors.OKBLUE + "Keeping Current Values")
        elif c.lower() == "a":
            global ai
            if ai:
                print("Ai Features deactivated")
                ai = False
            else:
                print(f"\033[93mGesture Mode Activated - Relaunching (Warning: Settings will be Reset)")
                print(f"\033[94m")
                ai = True
                pygame.quit()
                import gestures
        elif c.lower() == "h":
            print(bcolors.HEADER + "Please select the setting you'd like to change: ") 
            print(bcolors.OKBLUE + " 1 - Box Size ") 
            print(bcolors.OKBLUE + " 2 - # of Columns ") 
            print(bcolors.OKBLUE + " 3 - # of Rows") 
            print(bcolors.OKBLUE + " 4 - Advanced Random ") 
            print(bcolors.OKBLUE + " 5 - Waterfall Simulator ") 
            print(bcolors.OKBLUE + " 6 - Loop Back Mode ") 
            print() 
            print(bcolors.WARNING + " A - AI Gesture Mode (Erases Data)") 
            print() 
            print(bcolors.OKGREEN + " H - Help ") 
            print(bcolors.WARNING + " R - Reset to Defaults")
            print(bcolors.FAIL + " Q - Quit and Save")
        elif c.lower() == "r":
            print(bcolors.OKBLUE + "\nResetting Values to Default")
            sizeBox = 160
            font2 = pygame.font.Font('freesansbold.ttf', int(sizeBox/2-5))
            numBoxesX = 4
            numBoxesY = 4
            advancedRandom = False
            waterfall = False
            ai = False
            loopBack = False
            expandArray()
        elif c.lower() == "q":
            quitSet = True
            print(bcolors.OKBLUE + "Quiting...")
            initDisplay()
            resizeDisplay()
            initDisplay()
        else:
            print(LINE_UP + LINE_UP, end=LINE_CLEAR)
            noPress = True
        pygame.display.update()

## Actual game functionality
def checkSqaures(velX, velY):
    prevList = []
    for i in valList:
        arr = []
        for n in i:
            arr.append(n)
        prevList.append(arr)
    if velX == 0:
        if velY > 0:
            arrLoopBack = []
            if loopBack: ## LOOP BACK
                for i in range(numBoxesX):
                    arrLoopBack.append(valList[numBoxesY-1][i])
            for x in range(numBoxesX):
                nextEmpty = numBoxesY - 1
                for y in range(numBoxesY):
                    y = numBoxesY - y - 1
                    val = valList[y][x]
                    if val:
                        valList[y][x] = 0
                        valList[nextEmpty][x] = val
                        if nextEmpty + 1 < numBoxesY:
                            if val == valList[nextEmpty + 1][x]:
                                valList[nextEmpty][x] = 0
                                valList[nextEmpty + 1][x] = val + 1
                        nextEmpty = nextEmpty - 1
                nextEmpty = numBoxesY - 1
                for y in range(numBoxesY):
                    y = numBoxesY - y - 1
                    val = valList[y][x]
                    if val:
                        valList[y][x] = 0
                        valList[nextEmpty][x] = val
                        nextEmpty = nextEmpty - 1
            if loopBack: ## LOOP BACK
                for i in range(numBoxesX):
                    if not valList[0][i] and arrLoopBack[i] == valList[numBoxesY-1][i]:
                        valList[0][i] = arrLoopBack[i]
                        valList[numBoxesY-1][i] = 0
        else:
            arrLoopBack = []
            if loopBack: ## LOOP BACK
                for i in range(numBoxesX):
                    arrLoopBack.append(valList[0][i])
            for x in range(numBoxesX):
                nextEmpty = 0
                for y in range(numBoxesY):
                    val = valList[y][x]
                    if val:
                        valList[y][x] = 0
                        valList[nextEmpty][x] = val
                        if nextEmpty > 0:
                            if val == valList[nextEmpty - 1][x]:
                                valList[nextEmpty][x] = 0
                                valList[nextEmpty - 1][x] = val + 1
                        nextEmpty = nextEmpty + 1
                nextEmpty = 0
                for y in range(numBoxesY):
                    val = valList[y][x]
                    if val:
                        valList[y][x] = 0
                        valList[nextEmpty][x] = val
                        nextEmpty = nextEmpty + 1
            if loopBack: ## LOOP BACK
                for i in range(numBoxesX):
                    if not valList[numBoxesY-1][i] and arrLoopBack[i] == valList[0][i]:
                        valList[numBoxesY-1][i] = arrLoopBack[i]
                        valList[0][i] = 0
    elif velY == 0:
        if velX > 0:
            arrLoopBack = []
            if loopBack: ## LOOP BACK
                for i in range(numBoxesY):  # Switched from numBoxesX to numBoxesY
                    arrLoopBack.append(valList[i][numBoxesX-1])  # Changed indexing to switch axes
            for y in range(numBoxesY):
                nextEmpty = numBoxesX - 1
                for x in range(numBoxesX):
                    x = numBoxesX - x - 1
                    val = valList[y][x]
                    if val:
                        valList[y][x] = 0
                        valList[y][nextEmpty] = val
                        if nextEmpty + 1 < numBoxesX:
                            if val == valList[y][nextEmpty + 1]:
                                valList[y][nextEmpty] = 0
                                valList[y][nextEmpty + 1] = val + 1
                        nextEmpty = nextEmpty - 1
                nextEmpty = numBoxesX - 1
                for x in range(numBoxesX):
                    x = numBoxesX - x - 1
                    val = valList[y][x]
                    if val:
                        valList[y][x] = 0
                        valList[y][nextEmpty] = val
                        nextEmpty = nextEmpty - 1
            if loopBack: ## LOOP BACK
                for i in range(numBoxesY):  # Switched from numBoxesX to numBoxesY
                    if not valList[i][0] and arrLoopBack[i] == valList[i][numBoxesX-1]:
                        valList[i][0] = arrLoopBack[i]
                        valList[i][numBoxesX-1] = 0
        else:
            arrLoopBack = []
            if loopBack: ## LOOP BACK
                for i in range(numBoxesY):  # Switched from numBoxesX to numBoxesY
                    arrLoopBack.append(valList[i][0])  # Changed indexing to switch axes
            for y in range(numBoxesY):
                nextEmpty = 0
                for x in range(numBoxesX):
                    val = valList[y][x]
                    if val:
                        valList[y][x] = 0
                        valList[y][nextEmpty] = val
                        if nextEmpty > 0:
                            if val == valList[y][nextEmpty - 1]:
                                valList[y][nextEmpty] = 0
                                valList[y][nextEmpty - 1] = val + 1
                        nextEmpty = nextEmpty + 1
                nextEmpty = 0
                for x in range(numBoxesX):
                    val = valList[y][x]
                    if val:
                        valList[y][x] = 0
                        valList[y][nextEmpty] = val
                        nextEmpty = nextEmpty + 1
            if loopBack: ## LOOP BACK
                for i in range(numBoxesY):  # Switched from numBoxesX to numBoxesY
                    if not valList[i][numBoxesX-1] and arrLoopBack[i] == valList[i][0]:
                        valList[i][numBoxesX-1] = arrLoopBack[i]
                        valList[i][0] = 0
    else:
        print("Error In Config")
    deployed = False
    if prevList == valList:
        deployed = True
        if waterfall:
            deployed = False
    maxScore = max(map(max, valList))
    if maxScore == 11:
        global victory
        if not victory:
            print("VICTORY")
            global ai
            victory = True
    i = 0
    while(not deployed):
        i = i + 1
        x = round(random.random() * numBoxesX) - 1
        y = round(random.random() * numBoxesY) - 1
        if not valList[y][x]:
            rand = 0
            if advancedRandom:
                rand = math.floor(math.sqrt(random.random() * math.pow(maxScore,2))/2 + maxScore/2)
                if not rand:
                    rand = 1
            else:
                rand = 1
                if 1 == round(random.random())*10:
                    rand = 2
            valList[y][x] = rand
            deployed = True
        if i > numBoxesY * numBoxesX * 10:
            deployed = True
    renderGame()

resizeDisplay()
initDisplay()

def genFirst():
    x = round(random.random() * numBoxesX) - 1
    y = round(random.random() * numBoxesY) - 1
    valList[x][y] = 1

genFirst()
renderGame()
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                checkSqaures(-1,0)
            elif event.key == pygame.K_RIGHT:
                checkSqaures(1,0)
            elif event.key == pygame.K_DOWN:
                checkSqaures(0,1)
            elif event.key == pygame.K_UP:
                checkSqaures(0,-1)
            elif event.key == pygame.K_f or event.key == pygame.K_F11:
                if fullscreen:
                    pygame.display.set_mode((0,0),pygame.RESIZABLE)
                    fullscreen = False
                    resizeDisplay()
                else:
                    pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                    fullscreen = True

                initDisplay()
            elif event.key == pygame.K_RETURN:
                settingConfig()
            elif event.key == pygame.K_r:
                restartGame()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.VIDEORESIZE:
            resX, resY = pygame.display.get_window_size()
            initDisplay()
    if waterfall:
        checkSqaures(0,1)
    pygame.display.update()