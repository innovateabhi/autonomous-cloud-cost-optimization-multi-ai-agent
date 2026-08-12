from app.agents.utilization_agent import (
    UtilizationAgent
)

from app.agents.optimization_agent import (
    OptimizationAgent
)

from app.database.models import (
    Resource
)

from app.database.repositories.metrics_repository import (
    get_cpu_values
)

from app.database.session import SessionLocal


# --------------------------------------------------
# AGENTS
# --------------------------------------------------

utilization_agent = UtilizationAgent()

optimization_agent = OptimizationAgent()


# --------------------------------------------------
# GET RESOURCE FROM DATABASE
# --------------------------------------------------

def get_resource(
    resource_id
):
    """
    Retrieve a resource from PostgreSQL.

    resource_id refers to the PostgreSQL
    resources.id value.
    """

    db = SessionLocal()

    try:

        resource = (
            db.query(Resource)
            .filter(
                Resource.id == resource_id
            )
            .first()
        )

        return resource

    finally:

        db.close()


# --------------------------------------------------
# BUILD RESOURCE CONTEXT
# --------------------------------------------------

def build_resource_context(
    resource
):
    """
    Convert SQLAlchemy Resource object
    into the dictionary expected by
    the agents.
    """

    return {

        "resource_id":
            resource.resource_id,

        "resource_type":
            resource.resource_type,

        "name":
            resource.name,

        "region":
            resource.region,

        "state":
            resource.state,

        "instance_type":
            resource.instance_type,

        "environment":
            resource.environment,

        "tags":
            resource.tags or {}
    }


# --------------------------------------------------
# RUN OPTIMIZATION FOR ONE RESOURCE
# --------------------------------------------------

def analyze_resource(
    resource_id,
    hours=24,
    monthly_cost=None
):
    """
    Run the Utilization Agent followed by
    the Optimization Agent.

    Data flow:

    PostgreSQL
        ↓
    CPU metrics
        ↓
    Utilization Agent
        ↓
    Optimization Agent
    """

    print(
        "\n========================================"
    )

    print(
        "       RESOURCE OPTIMIZATION"
    )

    print(
        "========================================"
    )

    # --------------------------------------------------
    # FIND RESOURCE
    # --------------------------------------------------

    resource = get_resource(
        resource_id
    )

    if resource is None:

        raise ValueError(
            f"Resource with database ID "
            f"{resource_id} was not found."
        )

    print(
        f"Resource: "
        f"{resource.resource_id}"
    )

    print(
        f"Type: "
        f"{resource.resource_type}"
    )

    print(
        f"Instance type: "
        f"{resource.instance_type}"
    )

    # --------------------------------------------------
    # BUILD RESOURCE DATA
    # --------------------------------------------------

    resource_context = (
        build_resource_context(
            resource
        )
    )

    # --------------------------------------------------
    # GET CPU METRICS
    # --------------------------------------------------

    print(
        "\nFetching CPU metrics..."
    )

    cpu_values = get_cpu_values(

        resource_id=
            resource.id,

        hours=
            hours
    )

    print(
        f"CPU samples: "
        f"{len(cpu_values)}"
    )

    # --------------------------------------------------
    # RUN UTILIZATION AGENT
    # --------------------------------------------------

    print(
        "\nRunning Utilization Agent..."
    )

    utilization_result = (
        utilization_agent.run(
            {
                "cpu_values":
                    cpu_values
            }
        )
    )

    print(
        f"Utilization status: "
        f"{utilization_result.get('status')}"
    )

    # --------------------------------------------------
    # BUILD COST DATA
    # --------------------------------------------------

    if monthly_cost is not None:

        if monthly_cost >= 100:

            cost_level = "HIGH"

        elif monthly_cost >= 50:

            cost_level = "MEDIUM"

        else:

            cost_level = "LOW"

    else:

        cost_level = "UNKNOWN"

    cost_context = {

        "monthly_cost":
            monthly_cost,

        "cost_level":
            cost_level
    }

    # --------------------------------------------------
    # BUILD OPTIMIZATION CONTEXT
    # --------------------------------------------------

    optimization_context = {

        "resource":
            resource_context,

        "utilization":
            utilization_result,

        "cost":
            cost_context
    }

    # --------------------------------------------------
    # RUN OPTIMIZATION AGENT
    # --------------------------------------------------

    print(
        "\nRunning Optimization Agent..."
    )

    optimization_result = (
        optimization_agent.run(
            optimization_context
        )
    )

    # --------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------

    print(
        "\n========================================"
    )

    print(
        "       OPTIMIZATION RESULT"
    )

    print(
        "========================================"
    )

    print(
        f"Recommendation: "
        f"{optimization_result.get('recommendation')}"
    )

    print(
        f"Priority: "
        f"{optimization_result.get('priority')}"
    )

    print(
        f"Estimated savings: "
        f"${optimization_result.get('estimated_savings', 0)}"
    )

    print(
        f"Reason: "
        f"{optimization_result.get('reason')}"
    )

    # --------------------------------------------------
    # RETURN COMPLETE RESULT
    # --------------------------------------------------

    return {

        "resource":
            resource_context,

        "utilization":
            utilization_result,

        "cost":
            cost_context,

        "optimization":
            optimization_result
    }
