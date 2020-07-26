from snakeGameAi import main
from os import path

if __name__ == '__main__':
    local_dir = path.dirname(__file__)
    config_path = path.join(local_dir, "config-feedforward.txt")
    main.run(config_path)
