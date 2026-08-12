from collections import defaultdict

from app.database.session import SessionLocal

from app.database.models import Resource

from app.database.repositories.cost_repository import (
    get_unattributed_costs
)


def analyze_cost_attribution(
    days=30
):
    """
    Analyze AWS costs and determine whether
    they can currently be attributed to
    individual resources.

    IMPORTANT:
    Service-level Cost Explorer records are
    not automatically assigned to EC2
    instances without sufficient attribution
    information.
    """

    db = SessionLocal()

    try:

        # ==================================================
        # GET RESOURCES
        # ==================================================

        resources = (
            db.query(Resource)
            .filter(
                Resource.resource_type == "EC2"
            )
            .all()
        )

        # ==================================================
        # GET UNATTRIBUTED COSTS
        # ==================================================

        costs = get_unattributed_costs(
            session=db,
            days=days
        )

        # ==================================================
        # GROUP COSTS BY SERVICE
        # ==================================================

        service_totals = defaultdict(float)

        total_unattributed = 0.0

        for cost in costs:

            amount = float(
                cost.amount or 0
            )

            service_totals[
                cost.service
            ] += amount

            total_unattributed += amount

        # ==================================================
        # RESOURCE INFORMATION
        # ==================================================

        resource_results = []

        for resource in resources:

            resource_results.append({

                "resource_id":
                    resource.resource_id,

                "database_resource_id":
                    resource.id,

                "resource_type":
                    resource.resource_type,

                "instance_type":
                    resource.instance_type,

                "region":
                    resource.region,

                "state":
                    resource.state,

                "attributed_cost":
                    0.0,

                "cost_source":
                    "NONE",

                "confidence":
                    "NONE"
            })

        # ==================================================
        # FINAL RESULT
        # ==================================================

        return {

            "days":
                days,

            "resource_count":
                len(resources),

            "unattributed_record_count":
                len(costs),

            "total_unattributed_cost":
                round(
                    total_unattributed,
                    6
                ),

            "service_totals": {
                service: round(
                    amount,
                    6
                )
                for service, amount
                in service_totals.items()
            },

            "resources":
                resource_results
        }

    finally:

        db.close()
