from datetime import date, timedelta

from sqlalchemy import (
    select,
    func
)

from app.database.models import Cost


# ==================================================
# CREATE COST
# ==================================================

def create_cost(
    session,
    cost_data
):
    """
    Create a new cost record.
    """

    cost = Cost(

        resource_id=cost_data.get(
            "resource_id"
        ),

        service=cost_data["service"],

        cost_date=cost_data["cost_date"],

        amount=cost_data["amount"],

        currency=cost_data.get(
            "currency",
            "USD"
        )
    )

    session.add(cost)

    session.commit()

    session.refresh(cost)

    return cost


# ==================================================
# GET COSTS FOR SERVICE
# ==================================================

def get_costs_for_service(
    session,
    service
):
    """
    Retrieve all cost records for
    a specific AWS service.
    """

    statement = (

        select(Cost)

        .where(
            Cost.service == service
        )

        .order_by(
            Cost.cost_date
        )
    )

    return session.execute(
        statement
    ).scalars().all()


# ==================================================
# GET COSTS FOR RESOURCE
# ==================================================

def get_costs_for_resource(
    session,
    resource_id
):
    """
    Retrieve resource-specific costs.
    """

    statement = (

        select(Cost)

        .where(
            Cost.resource_id == resource_id
        )

        .order_by(
            Cost.cost_date
        )
    )

    return session.execute(
        statement
    ).scalars().all()


# ==================================================
# GET RESOURCE-SPECIFIC MONTHLY COST
# ==================================================

def get_resource_monthly_cost(
    session,
    resource_id,
    days=30
):
    """
    Calculate monthly cost for a
    specific resource.

    Returns None when no
    resource-specific billing data
    exists.
    """

    start_date = (
        date.today()
        - timedelta(days=days)
    )

    statement = (

        select(
            func.sum(Cost.amount)
        )

        .where(
            Cost.resource_id == resource_id
        )

        .where(
            Cost.cost_date >= start_date
        )
    )

    result = session.execute(
        statement
    ).scalar_one()

    if result is None:

        return None

    return float(result)


# ==================================================
# GET EC2 SERVICE MONTHLY COST
# ==================================================

def get_ec2_service_monthly_cost(
    session,
    days=30
):
    """
    Calculate total EC2 service-level
    cost over the last N days.

    This is NOT attributed to an
    individual EC2 instance.
    """

    start_date = (
        date.today()
        - timedelta(days=days)
    )

    statement = (

        select(
            func.sum(Cost.amount)
        )

        .where(
            Cost.service == "EC2 - Other"
        )

        .where(
            Cost.cost_date >= start_date
        )
    )

    result = session.execute(
        statement
    ).scalar_one()

    if result is None:

        return 0.0

    return float(result)


# ==================================================
# GET MONTHLY COST
# ==================================================

def get_monthly_cost(
    session,
    resource_id,
    days=30
):
    """
    Backward-compatible wrapper.

    Returns resource-specific cost
    when available.

    Otherwise returns None.
    """

    return get_resource_monthly_cost(
        session=session,
        resource_id=resource_id,
        days=days
    )

    # ==================================================
# GET UNATTRIBUTED COSTS
# ==================================================

def get_unattributed_costs(
    session,
    days=30
):
    """
    Retrieve cost records that are not yet
    attributed to a specific resource.
    """

    start_date = (
        date.today()
        - timedelta(days=days)
    )

    statement = (
        select(Cost)
        .where(
            Cost.resource_id.is_(None)
        )
        .where(
            Cost.cost_date >= start_date
        )
        .order_by(
            Cost.cost_date
        )
    )

    return session.execute(
        statement
    ).scalars().all()
