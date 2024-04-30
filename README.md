# 2048
A 2048 Game with AI gesture recognition powered by google mediapipe

# How to install
1. Download the files off of github
2. Run the setup.bat file if you're on windows or install `pygame` and `mediapipe` if you're not on windows (Shell scripts coming soon)
3. Run main.py
Then the game should be good to go.

# How to change the settings
1. Press enter
2. Go to the terminal that launched with the program
3. You should see something like this:
![image](https://github.com/NotAKerbal/2048/assets/5565682/4d37cd1e-d8ab-4ada-afee-8e3167999f84)

4. From there, you can select the command you desire by hitting the corresponding key. I've included a list of the commands and their functions below:

| Function Name         | Key | Description                                                                                                   |
|-----------------------|-----|---------------------------------------------------------------------------------------------------------------|
| Box Size              | 1   | Changes the size of the 2048 boxes                                                                            |
| # of Columns          | 2   | Changes the number of columns in your 2048 game                                                               |
| # of Rows             | 3   | Changes the number of rows in your 2048 game                                                                  |
| Max out Display       | 4   | Based on a resolution input maxes out the number of 2048 boxes that can fit on your screen                    |
| Advanced Random       | 5   | Allows more than just 2's and 4's to be generated                                                             |
| Waterfall Simulator   | 6   | Tells the computer to keep pressing down (Good for a video wall or fun experiments)                           |
| Loop Back Mode (Beta) | 7   | Causes the game to loop the bottom set of tiles to the top and so forth to make the game just a little harder |
| AI Gesture Mode       | A   | Switches the game to AI Gesture Mode (More on this later in the doc)                                          |
| Help                  | H   | Displays the list of commands again                                                                           |
| Reset to Defaults     | R   | Resets everything to their default values                                                                     |
| Quit and Save         | Q   | Quit the settings menu and save the settings                                                                  |

# AI Gesture Mode
This is an AI Gesture Mode that allows you to control your 2048 game with your hand. I'm using a library from google called [mediapipe]([url](https://mediapipe-studio.webapps.google.com/studio/demo/gesture_recognizer)). There are currently some bugs with the pygame window when you turn on this mode, so bear with me as I try to resolve them.

Eventually, I'll train my own gestures but for now, here's a list of the gestures used and what they do:

| Gesture     | Direction |
|-------------|-----------|
| Thumbs Up   | Up        |
| Thumbs Down | Down      |
| Closed Fist | Left      |
| Victory     | Right     |



# Enjoy!
