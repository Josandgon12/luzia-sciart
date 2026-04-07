import sys
sys.path.append('../luzia')

import json

import cv2
from luzia.analyzer import Analyzer

if __name__ == "__main__":
    analyzer = Analyzer(cv2.VideoCapture(0), capture_seconds=10, sleep_seconds=1)
    print(json.dumps(analyzer.analyze(), indent=2))
