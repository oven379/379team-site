"""Пересборка сайта: блог, услуги и YML. Запуск: python3 _tools/build_site.py."""
import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
for script in ["_tools/blog/build_blog.py", "_tools/pages/build_pages.py", "_tools/feed/build_feed.py"]:
    subprocess.run([sys.executable, str(root / script)], cwd=root, check=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
