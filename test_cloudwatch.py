from app.aws.ec2 import get_ec2_instances
from app.aws.cloudwatch import get_ec2_cpu_utilization


instances = get_ec2_instances()


if not instances:

    print("No EC2 instances found.")

else:

    for instance in instances:

        instance_id = instance["instance_id"]

        print("=" * 60)
        print(f"Instance: {instance_id}")
        print("=" * 60)

        datapoints = get_ec2_cpu_utilization(
            instance_id
        )

        if not datapoints:

            print("No CloudWatch metrics found.")

        else:

            for point in datapoints:

                timestamp = point["Timestamp"]
                average = point.get("Average")
                maximum = point.get("Maximum")

                print(
                    f"{timestamp} | "
                    f"Average CPU: {average:.2f}% | "
                    f"Maximum CPU: {maximum:.2f}%"
                )
