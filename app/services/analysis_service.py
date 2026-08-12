from app.database.models import Resource
from app.database.session import SessionLocal

from app.database.repositories.metrics_repository import (
    get_cpu_values
)

from app.database.repositories.cost_repository import (
    get_monthly_cost
)

from app.agents.utilization_agent import (
    UtilizationAgent
)

from app.agents.optimization_agent import (
    OptimizationAgent
)

from app.agents.risk_agent import (
    RiskAgent
)

from app.agents.execution_agent import (
    ExecutionAgent
)

# ==========================================================
# AGENTS
# ==========================================================

utilization_agent = UtilizationAgent()

optimization_agent = OptimizationAgent()

risk_agent = RiskAgent()

execution_agent = ExecutionAgent()


# ==========================================================
# ANALYZE SINGLE RESOURCE
# ==========================================================

def analyze_resource(
    db,
    resource,
    hours=24
):
    """
    Analyze a single cloud resource.

    Flow:

    PostgreSQL Resource
            ↓
    Metrics Repository
            ↓
    Utilization Agent
            ↓
    Cost Repository
            ↓
    Optimization Agent
            ↓
    Risk Agent
            ↓
    Execution Agent
            ↓
    Analysis Result
    """

    resource_id = resource.resource_id

    print(
        f"\nAnalyzing resource: "
        f"{resource_id}"
    )

    # ======================================================
    # RESOURCE DATA
    # ======================================================

    resource_context = {

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

    # ======================================================
    # FETCH CPU METRICS
    # ======================================================

    print(
        "Fetching CPU metrics..."
    )

    cpu_values = get_cpu_values(
        resource_id=resource.id,
        hours=hours
    )

    print(
        f"CPU samples found: "
        f"{len(cpu_values)}"
    )

    # ======================================================
    # UTILIZATION AGENT
    # ======================================================

    utilization_result = (
        utilization_agent.run(
            {
                "cpu_values":
                    cpu_values
            }
        )
    )

    print(
        f"CPU Status: "
        f"{utilization_result.get('status')}"
    )

    # ======================================================
    # MONTHLY COST
    # ======================================================

    monthly_cost = get_monthly_cost(
        session=db,
        resource_id=resource.id,
        days=30
    )

    # ======================================================
    # COST FALLBACK
    # ======================================================

    cost_source = "RESOURCE_COST"

    if monthly_cost is not None:

        monthly_cost = float(
            monthly_cost
        )

    else:

        monthly_cost = 7.59

        cost_source = "LOCAL_ESTIMATE"

    print(
        f"Estimated monthly cost: "
        f"${monthly_cost:.2f}"
    )

    print(
        f"Cost source: "
        f"{cost_source}"
    )

    # ======================================================
    # COST LEVEL
    # ======================================================

    if monthly_cost < 25:

        cost_level = "LOW"

    elif monthly_cost < 100:

        cost_level = "MEDIUM"

    else:

        cost_level = "HIGH"

    cost_result = {

        "monthly_cost":
            monthly_cost,

        "cost_level":
            cost_level,

        "cost_source":
            cost_source
    }

    # ======================================================
    # OPTIMIZATION AGENT
    # ======================================================

    optimization_context = {

        "resource":
            resource_context,

        "utilization":
            utilization_result,

        "cost":
            cost_result
    }

    optimization_result = (
        optimization_agent.run(
            optimization_context
        )
    )

    # ======================================================
    # RISK AGENT
    # ======================================================

    risk_context = {

        "resource":
            resource_context,

        "utilization":
            utilization_result,

        "optimization":
            optimization_result
    }

    risk_result = (
        risk_agent.run(
            risk_context
        )
    )

    # ======================================================
    # EXECUTION AGENT
    # ======================================================

    execution_context = {

        "resource":
            resource_context,

        "optimization":
            optimization_result,

        "risk":
            risk_result
    }

    execution_result = (
        execution_agent.run(
            execution_context
        )
    )

    # ======================================================
    # FINAL ANALYSIS RESULT
    # ======================================================

    result = {

        "resource":
            resource_context,

        "utilization":
            utilization_result,

        "cost":
            cost_result,

        "optimization":
            optimization_result,

        "risk":
            risk_result,

        "execution":
            execution_result
    }

    return result


# ==========================================================
# SYNCHRONIZE AWS RESOURCES
# ==========================================================

def synchronize_aws_resources():
    """
    Discover current AWS EC2 instances and synchronize
    them with PostgreSQL.

    New instances:
        INSERT

    Existing instances:
        UPDATE

    This function makes sure that every analysis run
    sees the latest EC2 infrastructure.
    """

    print()
    print("=" * 60)
    print("       AWS RESOURCE SYNCHRONIZATION")
    print("=" * 60)

    try:

        from app.aws.ec2 import (
            collect_and_save_ec2_instances
        )

        print()
        print(
            "Discovering EC2 instances from AWS..."
        )

        collect_and_save_ec2_instances()

        print()
        print(
            "✓ AWS → PostgreSQL synchronization completed."
        )

        return True

    except Exception as error:

        print()
        print(
            "✗ AWS resource synchronization failed."
        )

        print(
            f"Error: {error}"
        )

        # --------------------------------------------------
        # We don't immediately stop the whole analysis.
        # Existing PostgreSQL resources can still be analyzed.
        # --------------------------------------------------

        return False


# ==========================================================
# ANALYZE ALL RESOURCES
# ==========================================================

def analyze_all_resources(
    hours=24
):
    """
    Automatically:

    1. Discover current AWS EC2 resources.
    2. Synchronize them with PostgreSQL.
    3. Load all PostgreSQL resources.
    4. Analyze every resource.
    """

    # ======================================================
    # STEP 1 — AWS SYNCHRONIZATION
    # ======================================================

    sync_success = synchronize_aws_resources()

    if sync_success:

        print(
            "\n✓ Latest AWS resources are now available "
            "in PostgreSQL."
        )

    else:

        print(
            "\n⚠ AWS synchronization failed."
        )

        print(
            "Continuing with resources already "
            "stored in PostgreSQL."
        )

    # ======================================================
    # STEP 2 — DATABASE
    # ======================================================

    db = SessionLocal()

    results = []

    try:

        # ==================================================
        # FETCH RESOURCES
        # ==================================================

        resources = (
            db.query(Resource)
            .order_by(
                Resource.id
            )
            .all()
        )

        print()
        print(
            f"Resources found in PostgreSQL: "
            f"{len(resources)}"
        )

        # ==================================================
        # PROCESS EACH RESOURCE
        # ==================================================

        for resource in resources:

            try:

                result = analyze_resource(
                    db=db,
                    resource=resource,
                    hours=hours
                )

                results.append(
                    result
                )

            except Exception as error:

                print(
                    f"\n✗ Analysis failed for "
                    f"{resource.resource_id}"
                )

                print(error)

                # ------------------------------------------
                # Continue with remaining resources
                # ------------------------------------------

                results.append({

                    "resource": {

                        "resource_id":
                            resource.resource_id,

                        "resource_type":
                            resource.resource_type,

                        "instance_type":
                            resource.instance_type,

                        "region":
                            resource.region
                    },

                    "utilization": {},

                    "cost": {},

                    "optimization": {},

                    "risk": {},

                    "execution": {},

                    "error":
                        str(error)
                })

        # ==================================================
        # SUMMARY
        # ==================================================

        print()
        print(
            f"Resources analyzed: "
            f"{len(resources)}"
        )

        return results

    finally:

        db.close()
