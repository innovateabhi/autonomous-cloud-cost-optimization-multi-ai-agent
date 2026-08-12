from datetime import datetime, timedelta, timezone

from app.database.models import Metric
from app.database.session import SessionLocal


# ==================================================
# GET RECENT METRICS
# ==================================================

def get_recent_metrics(
    resource_id,
    hours=24
):
    """
    Retrieve recent metrics for a database
    resource.

    resource_id:
        PostgreSQL resources.id

    hours:
        Number of hours of historical metrics
        to retrieve.
    """

    db = SessionLocal()

    try:

        end_time = datetime.now(
            timezone.utc
        )

        start_time = (
            end_time
            - timedelta(hours=hours)
        )

        metrics = (
            db.query(Metric)

            .filter(
                Metric.resource_id
                == resource_id
            )

            .filter(
                Metric.timestamp
                >= start_time
            )

            .filter(
                Metric.timestamp
                <= end_time
            )

            .order_by(
                Metric.timestamp.asc()
            )

            .all()
        )

        return metrics

    finally:

        db.close()


# ==================================================
# GET CPU VALUES
# ==================================================

def get_cpu_values(
    resource_id,
    hours=24
):
    """
    Retrieve CPU average values for
    a resource.

    Returns:
        List of CPU average values.
    """

    metrics = get_recent_metrics(

        resource_id=
            resource_id,

        hours=
            hours
    )

    cpu_values = []

    for metric in metrics:

        if metric.cpu_average is not None:

            cpu_values.append(
                float(
                    metric.cpu_average
                )
            )

    return cpu_values


# ==================================================
# GET NETWORK VALUES
# ==================================================

def get_network_values(
    resource_id,
    hours=24
):
    """
    Retrieve NetworkIn and NetworkOut
    values for a resource.

    Returns:

        {
            "network_in": [...],
            "network_out": [...]
        }
    """

    metrics = get_recent_metrics(

        resource_id=
            resource_id,

        hours=
            hours
    )

    network_in = []

    network_out = []

    for metric in metrics:

        if metric.network_in is not None:

            network_in.append(
                float(
                    metric.network_in
                )
            )

        if metric.network_out is not None:

            network_out.append(
                float(
                    metric.network_out
                )
            )

    return {

        "network_in":
            network_in,

        "network_out":
            network_out
    }


# ==================================================
# GET LATEST METRIC
# ==================================================

def get_latest_metric(
    resource_id
):
    """
    Retrieve the most recent metric
    record for a resource.
    """

    db = SessionLocal()

    try:

        metric = (
            db.query(Metric)

            .filter(
                Metric.resource_id
                == resource_id
            )

            .order_by(
                Metric.timestamp.desc()
            )

            .first()
        )

        return metric

    finally:

        db.close()
