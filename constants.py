import re
import os

PATTERN = re.compile(r"avg send: (\d+),.*avg recv: (\d+)")
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
