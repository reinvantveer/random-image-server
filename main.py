import logging
import random
from argparse import ArgumentParser
from pathlib import Path

from flask import Flask, render_template, url_for

from common.config import load_config, Config


def main(config: Config):
    images_path_ = config['images']['path']
    app = Flask(__name__,
                static_url_path='/static',
                static_folder=images_path_)

    logging.info(f"Fetching image file list for {images_path_}")
    file_list = []

    for ext in config['images']['filetypes']:
        file_list.extend(Path(images_path_).rglob(ext))

    logging.info('Building list')
    file_list = list(file_list)

    @app.route("/")
    def hello() -> str:
        random_img = random.randint(0, len(file_list))
        img_path = file_list[random_img]
        img_relative_to_static_folder = str(img_path).replace(images_path_, '/static')
        return render_template("index.html", user_image=img_relative_to_static_folder, local_path=img_path)

    app.run()


if __name__ == '__main__':
    parser = ArgumentParser('Serves images from the folder provided in config.yaml')
    parser.add_argument('-c', '--config', default='config.yaml')

    args = parser.parse_args()
    config = load_config(args.config)

    main(config)
