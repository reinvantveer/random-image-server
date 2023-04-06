import random
from argparse import ArgumentParser
from pathlib import Path

from flask import Flask

from common.config import load_config

app = Flask(__name__)


if __name__ == '__main__':
    parser = ArgumentParser('Serves images from the folder provided in config.yaml')
    parser.add_argument('-c', '--config', default='config.yaml')

    args = parser.parse_args()
    config = load_config(args.config)

    file_list = []
    for ext in config['images']['filetypes']:
        file_list.extend(Path(config['images']['path']).glob(ext))

    @app.route("/")
    def hello() -> str:
        random_img = random.randint(0, len(file_list))
        return f"<img src={random_img}>Hello</img>"

    app.run()
