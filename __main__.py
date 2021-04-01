import os
from conf.config import Config
from app import App
import conf
import logging as log
import pandas as pd

if __name__ == '__main__':
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        path_to_conf = os.path.join(path, "conf.ini")
        conf = Config(path_to_conf)
        print("conf....", conf.basic.get('EMAIL_LIST'))
        log.info(f'getting configuration....{conf.basic}')
        app = App(conf)
        app.run()
        df = pd.read_csv(r'C:\Users\kushakj\Downloads\592e5dc8-a1cf-4e5e-adb7-bdcca8581874.csv')
        print("df...", df.head(10))
    except Exception as exc:
        log.info(f'Exception occured while running app..{exc}')

