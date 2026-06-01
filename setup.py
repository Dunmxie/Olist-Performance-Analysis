import os

folders = [
    "data/raw",
    "data/cleaned",
    "data/sql",
    "notebooks/01_cleaning",
    "notebooks/02_eda",
    "notebooks/03_sql_validation",
    "notebooks/04_forecasting",
    "reports/dashboard_exports",
    "reports/exec_deck",
    "reports/memo",
    "sql/views",
    "sql/queries",
    "sql/schema",
    "src",
    "docs"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    gitkeep = os.path.join(folder, ".gitkeep")
    if not os.listdir(folder):
        with open(gitkeep, "w") as f:
            pass

print("Project scaffold created successfully.")
