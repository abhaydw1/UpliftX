"""Central place for paths and constants. Every other script imports from here."""
from pathlib import Path

# ---------- Paths (built from this file's location, so they work from anywhere) ----------
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
SQL_DIR = ROOT_DIR / "sql"
FIGURES_DIR = ROOT_DIR / "reports" / "figures"

DB_PATH = DATA_DIR / "uplift.db"   # SQLite database (git-ignored)
TABLE_NAME = "customers"

# ---------- Reproducibility ----------
RANDOM_SEED = 42
TEST_SIZE = 0.30                   # 70/30 train/test split

# ---------- Business assumptions ----------
OFFER_COST = 20                    # Rs per contact (change here to test sensitivity)
TOP_K_VALUES = [0.10, 0.20, 0.30]  # for uplift@k evaluation

# ---------- Experiment definition ----------
CONTROL_LABEL = "No E-Mail"        # anything else in `segment` counts as treated
