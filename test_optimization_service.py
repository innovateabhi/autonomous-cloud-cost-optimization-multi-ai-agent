from app.services.optimization_service import (
    analyze_resource
)

from app.database.models import Resource
from app.database.session import SessionLocal


print("\n========================================")
print("    OPTIMIZATION SERVICE TEST")
print("========================================\n")


# --------------------------------------------------
# FIND FIRST RESOURCE
# --------------------------------------------------

db = SessionLocal()

try:

    resource = (
        db.query(Resource)
        .first()
    )

finally:

    db.close()


if resource is None:

    print(
        "No resources found in database."
    )

    print(
        "Run EC2 resource discovery first."
    )

    exit(1)


print(
    f"Database Resource ID: "
    f"{resource.id}"
)

print(
    f"AWS Instance ID: "
    f"{resource.resource_id}"
)


# --------------------------------------------------
# RUN COMPLETE ANALYSIS
# --------------------------------------------------

result = analyze_resource(

    resource_id=
        resource.id,

    hours=
        24
)


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

print(
    "\n========================================"
)

print(
    "       FINAL SERVICE RESULT"
)

print(
    "========================================\n"
)

print(
    "UTILIZATION:"
)

print(
    result["utilization"]
)

print(
    "\nOPTIMIZATION:"
)

print(
    result["optimization"]
)

print(
    "\n========================================"
)

print(
    "       TEST COMPLETED"
)

print(
    "========================================\n"
)
