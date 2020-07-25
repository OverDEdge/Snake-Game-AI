# Snake Game
This is a Snake Game made in Pygame.
Necessary packages:

- **Pygame**

## Game mechanics
The snake is controlled by using the arrow keys (**UP**, **DOWN**, **LEFT** and **RIGHT**) or **'a'** = Left, **'s'** = Down, **'d'** = Right, **'w'** = Up on the keyboard.

When the snake eats an apple it will grow by one square and a new apple will pop up at a random location on the screen. The apple will move randomly in any direction one square every second.

It is Game Over if the snake hits a wall or collides with it's own body so be careful :).

The Highscore is saved in a separate text file:
- *highscore.txt*

If you want to reset the Highscore you can just delete this file. A new file will be created if it doesn't exist with score at zero.

### Aim of the game
The aim of the game is to eat apples and get as high a score as possible. For every apple the score is increased by 10.

At every step of 50 points the snake will speed up, reaching the max speed at (currently) 350 points.

## How to start the application
Download a copy of the repository into a folder named 'snake'. Navigate to location where newly created 'snake' folder is located. In Command Prompt type:

```
python -m snake
```

This will start the game and game will launch in a separate window. *'ESC'* or pressing the *'x'* at top right can be used to exit the application at any time.
