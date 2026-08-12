from sqlalchemy import select

from app.database.models import Metric


def create_metric(
    session,
    metric_data
):

    metric = Metric(

        resource_id=metric_data["resource_id"],

        timestamp=metric_data["timestamp"],

        cpu_average=metric_data.get(
            "cpu_average"
        ),

        cpu_maximum=metric_data.get(
            "cpu_maximum"
        ),

        cpu_minimum=metric_data.get(
            "cpu_minimum"
        ),

        network_in=metric_data.get(
            "network_in"
        ),

        network_out=metric_data.get(
            "network_out"
        ),

        disk_read=metric_data.get(
            "disk_read"
        ),

        disk_write=metric_data.get(
            "disk_write"
        )
    )

    session.add(metric)

    session.commit()

    session.refresh(metric)

    return metric


def get_metrics_for_resource(
    session,
    resource_id
):

    statement = (
        select(Metric)
        .where(
            Metric.resource_id == resource_id
        )
        .order_by(
            Metric.timestamp
        )
    )

    return session.execute(
        statement
    ).scalars().all()
