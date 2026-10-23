# backend/settings/__init__.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Path to root directory (where manage.py lives)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env.local if present, otherwise load .env
env_local = BASE_DIR / ".env.local"
env_default = BASE_DIR / ".env"

if env_local.exists():
    load_dotenv(BASE_DIR / ".env.local", override=True)
elif env_default.exists():
    load_dotenv(env_default)

raw_debug = os.getenv("DEBUG", "False").strip().strip('"').strip("'").lower()
is_debug = raw_debug in ("true", "1", "t", "yes", "on")



if is_debug:
    from .local import *
else:
    from .prod import *