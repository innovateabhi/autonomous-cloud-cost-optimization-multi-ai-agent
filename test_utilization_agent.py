from app.database.repositories.metrics_repository import (
    get_cpu_values
)

from app.agents.utilization_agent import (
    UtilizationAgent
)

from app.database.models import Resource
from app.database.session import SessionLocal


print("\n========================================")
print("      UTILIZATION AGENT TEST")
print("========================================\n")


# --------------------------------------------------
# FIND A RESOURCE FROM DATABASE
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
    f"Resource ID: {resource.id}"
)

print(
    f"AWS Instance: {resource.resource_id}"
)

print(
    f"Region: {resource.region}"
)


# --------------------------------------------------
# FETCH REAL CPU METRICS
# --------------------------------------------------

print(
    "\nFetching CPU metrics from "
    "PostgreSQL..."
)


cpu_values = get_cpu_values(
    resource_id=resource.id,
    hours=24
)


print(
    f"CPU samples found: "
    f"{len(cpu_values)}"
)


if not cpu_values:

    print(
        "\nNo CPU metrics available."
    )

    print(
        "Run test_metrics_service.py "
        "first."
    )

    exit(1)


# --------------------------------------------------
# RUN UTILIZATION AGENT
# --------------------------------------------------

agent = UtilizationAgent()


result = agent.run(
    {
        "cpu_values": cpu_values
    }
)


# --------------------------------------------------
# DISPLAY RESULT
# --------------------------------------------------

print(
    "\n========================================"
)

print(
    "       UTILIZATION RESULT"
)

print(
    "========================================\n"
)

print(
    f"Status          : "
    f"{result.get('status')}"
)

print(
    f"Average CPU     : "
    f"{result.get('average_cpu')}%"
)

print(
    f"Minimum CPU     : "
    f"{result.get('minimum_cpu')}%"
)

print(
    f"Maximum CPU     : "
    f"{result.get('maximum_cpu')}%"
)

print(
    f"Samples         : "
    f"{result.get('samples')}"
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
