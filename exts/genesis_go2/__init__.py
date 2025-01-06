"""
Python module serving as a project/extension template.
"""

import os
import toml

GENESIS_GO2_EXT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
GENESIS_GO2_MODEL_DIR = os.path.join(GENESIS_GO2_EXT_DIR, "model")

# RL environments.
from .env import *

# Robot Model
from .model import *
