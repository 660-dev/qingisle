import os
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
# load env from project root
os.chdir(root.parent if (root.parent / ".env").exists() or (root.parent / ".env.local").exists() else root)
sys.path.insert(0, str(root))
from app.main import run
run()
