from app.aws.cloudwatch import (
    get_ec2_cpu_utilization,
    get_ec2_network_metrics
)

from app.database.models import (
    Resource,
    Metric
)

from app.database.session import SessionLocal


def collect_ec2_metrics(
    resource_id,
    region,
    hours=24
):
    """
    Collect CloudWatch metrics for an EC2
    instance and save them to PostgreSQL.

    resource_id:
        AWS EC2 instance ID, e.g. i-0123456789

    region:
        AWS region, e.g. ap-south-2
    """

    print(
        f"\nCollecting metrics for "
        f"{resource_id}..."
    )

    # --------------------------------------------------
    # DATABASE SESSION
    # --------------------------------------------------

    db = SessionLocal()

    try:

        # --------------------------------------------------
        # FIND RESOURCE IN DATABASE
        # --------------------------------------------------

        resource = (
            db.query(Resource)
            .filter(
                Resource.resource_id
                == resource_id
            )
            .first()
        )

        if resource is None:

            raise ValueError(
                f"Resource {resource_id} "
                "was not found in the "
                "resources table."
            )

        database_resource_id = resource.id

        print(
            f"Database resource ID: "
            f"{database_resource_id}"
        )

        # --------------------------------------------------
        # CPU METRICS
        # --------------------------------------------------

        cpu_datapoints = (
            get_ec2_cpu_utilization(
                instance_id=resource_id,
                region=region,
                hours=hours
            )
        )

        # --------------------------------------------------
        # NETWORK METRICS
        # --------------------------------------------------

        network_metrics = (
            get_ec2_network_metrics(
                instance_id=resource_id,
                region=region,
                hours=hours
            )
        )

        network_in_datapoints = (
            network_metrics.get(
                "NetworkIn",
                []
            )
        )

        network_out_datapoints = (
            network_metrics.get(
                "NetworkOut",
                []
            )
        )

        print(
            f"CPU datapoints: "
            f"{len(cpu_datapoints)}"
        )

        print(
            f"NetworkIn datapoints: "
            f"{len(network_in_datapoints)}"
        )

        print(
            f"NetworkOut datapoints: "
            f"{len(network_out_datapoints)}"
        )

        # --------------------------------------------------
        # BUILD NETWORK LOOKUPS
        # --------------------------------------------------

        network_in = {}

        for datapoint in network_in_datapoints:

            timestamp = datapoint.get(
                "Timestamp"
            )

            if timestamp:

                network_in[timestamp] = (
                    datapoint.get("Average")
                )

        network_out = {}

        for datapoint in network_out_datapoints:

            timestamp = datapoint.get(
                "Timestamp"
            )

            if timestamp:

                network_out[timestamp] = (
                    datapoint.get("Average")
                )

        # --------------------------------------------------
        # PROCESS CPU DATAPOINTS
        # --------------------------------------------------

        saved_count = 0

        for datapoint in cpu_datapoints:

            timestamp = datapoint.get(
                "Timestamp"
            )

            if timestamp is None:
                continue

            # ------------------------------------------
            # CHECK WHETHER METRIC ALREADY EXISTS
            # ------------------------------------------

            metric = (
                db.query(Metric)
                .filter(
                    Metric.resource_id
                    == database_resource_id
                )
                .filter(
                    Metric.timestamp
                    == timestamp
                )
                .first()
            )

            # ------------------------------------------
            # CREATE NEW METRIC
            # ------------------------------------------

            if metric is None:

                metric = Metric(

                    resource_id=
                        database_resource_id,

                    timestamp=
                        timestamp,

                    cpu_average=
                        datapoint.get(
                            "Average"
                        ),

                    cpu_maximum=
                        datapoint.get(
                            "Maximum"
                        ),

                    cpu_minimum=
                        datapoint.get(
                            "Minimum"
                        ),

                    network_in=
                        network_in.get(
                            timestamp
                        ),

                    network_out=
                        network_out.get(
                            timestamp
                        )
                )

                db.add(metric)

                saved_count += 1

            # ------------------------------------------
            # UPDATE EXISTING METRIC
            # ------------------------------------------

            else:

                metric.cpu_average = (
                    datapoint.get(
                        "Average"
                    )
                )

                metric.cpu_maximum = (
                    datapoint.get(
                        "Maximum"
                    )
                )

                metric.cpu_minimum = (
                    datapoint.get(
                        "Minimum"
                    )
                )

                metric.network_in = (
                    network_in.get(
                        timestamp
                    )
                )

                metric.network_out = (
                    network_out.get(
                        timestamp
                    )
                )

        # --------------------------------------------------
        # NETWORK-ONLY DATAPOINTS
        # --------------------------------------------------

        cpu_timestamps = {
            datapoint.get("Timestamp")
            for datapoint in cpu_datapoints
            if datapoint.get("Timestamp")
        }

        network_timestamps = (
            set(network_in.keys())
            | set(network_out.keys())
        )

        network_only_timestamps = (
            network_timestamps
            - cpu_timestamps
        )

        for timestamp in network_only_timestamps:

            metric = Metric(

                resource_id=
                    database_resource_id,

                timestamp=
                    timestamp,

                network_in=
                    network_in.get(
                        timestamp
                    ),

                network_out=
                    network_out.get(
                        timestamp
                    )
            )

            db.add(metric)

            saved_count += 1

        # --------------------------------------------------
        # COMMIT
        # --------------------------------------------------

        db.commit()

        print(
            f"✓ Metrics saved successfully."
        )

        print(
            f"✓ New records created: "
            f"{saved_count}"
        )

    except Exception as error:

        db.rollback()

        print(
            "\n✗ Metrics collection failed:"
        )

        print(error)

        raise

    finally:

        db.close()


def collect_metrics_for_all_resources(
    resources,
    hours=24
):
    """
    Collect metrics for all supplied
    EC2 resources.

    Supports resources returned by
    app.aws.ec2.get_ec2_instances(),
    where the AWS instance ID is stored
    as 'instance_id'.
    """

    print(
        "\n========================================"
    )

    print(
        "       METRICS COLLECTION"
    )

    print(
        "========================================"
    )

    for resource in resources:

        # --------------------------------------------------
        # GET AWS EC2 INSTANCE ID
        # --------------------------------------------------

        resource_id = resource.get(
            "resource_id"
        )

        # AWS discovery returns instance_id
        if not resource_id:

            resource_id = resource.get(
                "instance_id"
            )

        # --------------------------------------------------
        # GET REGION
        # --------------------------------------------------

        region = resource.get(
            "region"
        )

        # --------------------------------------------------
        # VALIDATE RESOURCE ID
        # --------------------------------------------------

        if not resource_id:

            print(
                "⚠ Skipping resource: "
                "resource_id/instance_id missing."
            )

            continue

        # --------------------------------------------------
        # VALIDATE REGION
        # --------------------------------------------------

        if not region:

            print(
                f"⚠ Skipping {resource_id}: "
                "region missing."
            )

            continue

        # --------------------------------------------------
        # COLLECT METRICS
        # --------------------------------------------------

        try:

            collect_ec2_metrics(

                resource_id=
                    resource_id,

                region=
                    region,

                hours=
                    hours
            )

        except Exception as error:

            print(
                f"✗ Failed for "
                f"{resource_id}:"
            )

            print(error)

    print(
        "\n========================================"
    )

    print(
        "     METRICS COLLECTION COMPLETE"
    )

    print(
        "========================================"
    )
