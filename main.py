import pygame
import math
import random
import os
import platform
import tkinter
import customtkinter
import screeninfo
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

##Game Settings
sizeBox = 160
spaceBox = 2
numBoxesX = 4
numBoxesY = 4
advancedRandom = False
aiOption = "None"

## Important Variables
endOfGameX = 10 + numBoxesX * (spaceBox + sizeBox)
endOfGameY = 10 + numBoxesY * (spaceBox + sizeBox)
maxScore = 0
bottomOfHeader = 10
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
pygame.display.set_caption(name)
font = pygame.font.Font('freesansbold.ttf', 15)
font2 = pygame.font.Font('freesansbold.ttf', int(sizeBox/2-5))

clock = pygame.time.Clock()

def initPyGame():
    pygame.init()
    global gameDisplay, endOfGameX, endOfGameY, font, font2, clock
    endOfGameX = 10 + numBoxesX * (spaceBox + sizeBox)
    endOfGameY = 10 + numBoxesY * (spaceBox + sizeBox)
    resizeDisplay()
    pygame.display.set_caption(name)
    font2 = pygame.font.Font('freesansbold.ttf', int(sizeBox/2-5))
    clock = pygame.time.Clock()
    gameDisplay.fill(background)
    renderGame()

def resizeDisplay():
    if not fullscreen:
        global endOfGameX, endOfGameY, resX, resY
        endOfGameX = 10 + numBoxesX * (spaceBox + sizeBox)
        endOfGameY = 10 + numBoxesY * (spaceBox + sizeBox)
        resX = endOfGameX + 10
        resY = endOfGameY + 10
        pygame.display.set_mode((resX,resY),pygame.RESIZABLE)

crashed = False

def drawBox(num,x,y):
    global spacing
    colNum = num % 12
    color = colorList[colNum]
    pygame.draw.rect(gameDisplay,color,pygame.Rect(10+x*spacing,10+y*spacing,sizeBox,sizeBox),border_radius=round(sizeBox/16))
    if num > 0 and sizeBox > 40:
        text = font2.render(str(round(math.pow(2,num))), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (10+x*spacing+sizeBox/2, 10+y*spacing+sizeBox/2)
        gameDisplay.blit(text, textRect)


def renderGame():
    gameDisplay.fill(background)
    global spacing
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


class Settings(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        global sizeBox, numBoxesX, numBoxesY, advancedRandom, loopBack, aiOption
        self.geometry("840x800")
        self.title("Settings")
        self.minsize(300, 200)
        self.font = customtkinter.CTkFont(family="roboto",size=32)

        self.bSFrame = customtkinter.CTkFrame(master=self )
        self.bSFrame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.bSFrame.sizingLabel = customtkinter.CTkLabel(self.bSFrame, text="Sizing Controls",font=self.font)
        self.bSFrame.sizingLabel.grid(row=0,column=0,columnspan = 2,pady=20)
        # Box Size
        self.bSFrame.boxSizeLabel = customtkinter.CTkLabel(self.bSFrame, text="Box Size: " + str(sizeBox), fg_color="transparent",font=self.font)
        self.bSFrame.boxSizeLabel.grid(row=1, column=0,sticky="w",padx=20)

       
        def update_box_size(value):
            global sizeBox
            sizeBox = round(value/10)*10
            self.bSFrame.boxSizeLabel.configure(text="Box Size: " + str(sizeBox))
            self.bSFrame.boxSizeSlider.set(sizeBox)
        
        self.bSFrame.boxSizeSlider = customtkinter.CTkSlider(self.bSFrame, from_=10, to=200, command=update_box_size,height=32,width=360)
        self.bSFrame.boxSizeSlider.grid(row=1, column=1,sticky="e",padx=20,pady=20)

        #X Value
        self.bSFrame.xLabel = customtkinter.CTkLabel(self.bSFrame, text="Number of Columns: " + str(numBoxesX), fg_color="transparent",font=self.font)
        self.bSFrame.xLabel.grid(row=2, column=0,sticky="w",padx=20,pady=20)

        def update_x(value):
            global numBoxesX
            numBoxesX = round(value)
            self.bSFrame.xLabel.configure(text="Number of Columns: " + str(numBoxesX))
            self.bSFrame.xSlider.set(numBoxesX)
        
        self.bSFrame.xSlider = customtkinter.CTkSlider(self.bSFrame, from_=1, to=100, command=update_x,height=32,width=360)
        self.bSFrame.xSlider.grid(row=2, column=1,sticky="e",padx=20,pady=20)

        #Y Value
        self.bSFrame.yLabel = customtkinter.CTkLabel(self.bSFrame, text="Number of Rows: " + str(numBoxesY), fg_color="transparent",font=self.font)
        self.bSFrame.yLabel.grid(row=3, column=0, padx=20, pady=20, sticky="w")

        def update_y(value):
            global numBoxesY
            numBoxesY = round(value)
            self.bSFrame.yLabel.configure(text="Number of Rows: " + str(numBoxesY))
            self.bSFrame.ySlider.set(numBoxesY)
        

        self.bSFrame.ySlider = customtkinter.CTkSlider(self.bSFrame, from_=1, to=100, command=update_y,height=32,width=360)
        self.bSFrame.ySlider.grid(row=3, column=1)

        #autofit Screen
        def autofit_screen_event():
            monitor_info = screeninfo.get_monitors()
            monitor = 0
            if not len(monitor_info) == 1:
                monitor = -1
            global numBoxesX, numBoxesY, sizeBox, spaceBox
            update_x(math.floor((monitor_info[monitor].width - (10)) / (sizeBox + spaceBox)))
            update_y(math.floor((monitor_info[monitor].height - (10)) / (sizeBox + spaceBox)))
            expandArray()
            

        
        self.autofitButton = customtkinter.CTkButton(self.bSFrame,text="Autofit Screen",command=autofit_screen_event, font=self.font)
        self.autofitButton.grid(row=4,column=0,sticky="w",padx=20, pady=20)

        #Random Modes
        self.rFrame = customtkinter.CTkFrame(master=self, width=760, height=200)
        self.rFrame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

        self.rFrame.labelRandom = customtkinter.CTkLabel(self.rFrame, text="Random Settings",fg_color="transparent",font=self.font,width=800)
        self.rFrame.labelRandom.grid(row=0,column=0,sticky="ew",pady=20)
        def ai_options_callback(value):
            print("segmented button clicked:", value)

        segemented_button_var = customtkinter.StringVar(value="Normal")
        self.segemented_button = customtkinter.CTkSegmentedButton(self, values=["Normal", "Hard", "Insane"],
                                                     command=ai_options_callback,
                                                     variable=segemented_button_var)

        self.oFrame = customtkinter.CTkFrame(master=self, width=760, height=200)
        self.oFrame.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")

        #Loop Back
        def switch_loopback():
            global loopBack
            loopBack = switch_var_loopBack.get()

        switch_var_loopBack = customtkinter.BooleanVar(value=False)
        self.switchLoopBack = customtkinter.CTkSwitch(self.oFrame, text="Loopback Mode (Beta)", command=switch_loopback,variable=switch_var_loopBack, onvalue=True, offvalue=False,font=self.font,height=32)
        self.switchLoopBack.grid(row=0,column=0,pady=20,padx=20)

        self.aFrame = customtkinter.CTkFrame(master=self, width=760, height=200)
        self.aFrame.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")

        self.aiOptionsLabel = customtkinter.CTkLabel(master=self.aFrame,text="AI Options",font=self.font)
        self.aiOptionsLabel.grid(row=0,column=0,padx=20,pady=20)

        def ai_options_callback(value):
            global aiOption
            aiOption = value
        self.aiOptions = customtkinter.CTkSegmentedButton(self.aFrame, values=["None", "Waterfall", "Smart"],command=ai_options_callback, font=self.font)
        self.aiOptions.grid(row=0,column=1,padx=20,pady=20)

        #AI Mode
        def ai_button_event():
            pygame.quit()
            self.destroy()
            os.system("python gestures.py")

        self.uFrame = customtkinter.CTkFrame(master=self, width=760, height=200)
        self.uFrame.grid(row=6, column=0, padx=20, pady=20, sticky="nsew")

        self.aiButton = customtkinter.CTkButton(self.uFrame, text="Gesture Mode", command=ai_button_event, font=self.font)
        self.aiButton.grid(row=0,column=0,sticky="w",padx=20, pady=20)
        def reset_button_event():
            global sizeBox, font2, numBoxesX, numBoxesY, advancedRandom, ai, loopBack
            sizeBox = 160
            font2 = pygame.font.Font('freesansbold.ttf', int(sizeBox/2-5))
            numBoxesX = 4
            numBoxesY = 4
            advancedRandom = False
            ai = False
            loopBack = False
            aiOption = "None"
            expandArray()
            update_box_size(sizeBox)
            update_x(numBoxesX)
            update_y(numBoxesY)
            switch_var_loopBack.set(loopBack)
            self.aiOptions.set(aiOption)
        
        self.resetButton = customtkinter.CTkButton(self.uFrame, text= "Reset Settings", command=reset_button_event, font=self.font)
        self.resetButton.grid(row=0,column=1,sticky="w",padx=20, pady=20)

        def exit_button_event():
            self.destroy()
        
        self.exitButton = customtkinter.CTkButton(self.uFrame,text="Save and Exit",command=exit_button_event, font=self.font)
        self.exitButton.grid(row=0,column=2,sticky="w",padx=20, pady=20)

        update_box_size(sizeBox)
        update_x(numBoxesX)
        update_y(numBoxesY)
        switch_var_loopBack.set(loopBack)
        self.aiOptions.set(aiOption)


    
    

def settingConfig():
    settings = Settings()
    settings.mainloop()
    #font2 = pygame.font.Font('freesansbold.ttf', int(sizeBox/2-5))
    expandArray()
    resizeDisplay()
    gameDisplay.fill(background)
    renderGame()
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
        if aiOption == "Waterfall":
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
count = 0
def calcMove():
    global count
    if count == 0:
        checkSqaures(0,1)
        count = 1
    elif count == 1:
        checkSqaures(1,0)
        count = 2
    elif count == 2:
        checkSqaures(0,-1)
        count = 3
    elif count == 3:
        checkSqaures(-1,0)
        count = 0

def genFirst():
    x = round(random.random() * numBoxesX) - 1
    y = round(random.random() * numBoxesY) - 1
    valList[x][y] = 1

resizeDisplay()
gameDisplay.fill(background)
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
                renderGame()
            elif event.key == pygame.K_RETURN:
                settingConfig()
            elif event.key == pygame.K_r:
                restartGame()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.VIDEORESIZE:
            resX, resY = pygame.display.get_window_size()
            renderGame()
    if aiOption == "Waterfall":
        checkSqaures(0,1)
    elif aiOption == "Smart":
        calcMove()
    pygame.display.update()
