from os import path
from . import settings

def generate_map():
    with open(path.join(settings.IMG_FOLDER, settings.MAP_IMG), 'w') as f:
        for i in range(settings.GRIDHEIGHT):
            for j in range(settings.GRIDWIDTH):
                if i == 0 or i == settings.GRIDHEIGHT - 1:
                    f.write('1' * settings.GRIDWIDTH +'\n')
                    break

                if j == 0 or j == settings.GRIDWIDTH - 1:
                    f.write('1')
                elif i == settings.SNAKE_START_POS[0] and j == settings.SNAKE_START_POS[1]:
                    f.write('S')
                else:
                    f.write('0')
            else:
                f.write('\n')
