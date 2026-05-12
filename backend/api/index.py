import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:////tmp/designer_agent.db")
os.environ["VERCEL"] = "1"

import shutil
tmp_db = "/tmp/designer_agent.db"
if not os.path.exists(tmp_db):
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "designer_agent.db")
    if os.path.exists(src):
        shutil.copy2(src, tmp_db)

# Patch scheduler to no-op on Vercel
import app.scheduler
app.scheduler.start_scheduler = lambda: None
app.scheduler.stop_scheduler = lambda: None

from app.main import app
handler = app
