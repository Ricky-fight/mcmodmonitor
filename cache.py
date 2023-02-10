import logging
import pickle
import config
from pathlib import Path

logger = logging.Logger(__name__)


class FingerPrintCache:
    def __init__(self, inputFile="fingerprint.cache"):
        self.filename = inputFile
        try:
            with open(inputFile, "rb") as f:
                self.filename = f.name
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}
        except EOFError:
            self.data = {}

    def save(self):
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.data, f)
        except IOError as e:
            logger.error(e, f"发生IO错误，无法写入缓存文件{f.name}")
