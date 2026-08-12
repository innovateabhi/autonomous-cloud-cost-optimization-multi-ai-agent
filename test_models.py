from sqlalchemy import inspect

from app.database.connection import engine

from app.database.models import (
    Resource,
    Metric,
    Cost,
    Recommendation,
    Action
)


inspector = inspect(engine)


tables = inspector.get_table_names()


expected_tables = [
    "resources",
    "metrics",
    "costs",
    "recommendations",
    "actions"
]


print("Checking database tables...")
print()


for table in expected_tables:

    if table in tables:

        print(f"✓ {table}")

    else:

        print(f"✗ {table}")


print()
print("SQLAlchemy models loaded successfully.")
