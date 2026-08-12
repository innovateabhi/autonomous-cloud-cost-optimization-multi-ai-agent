from app.aws.ec2 import get_ec2_instances


instances = get_ec2_instances()


if not instances:
    print("No EC2 instances found.")

else:
    print("EC2 INSTANCES")
    print("=" * 50)

    for instance in instances:
        print(f"Instance ID   : {instance['instance_id']}")
        print(f"Instance Type : {instance['instance_type']}")
        print(f"State         : {instance['state']}")
        print(f"Region        : {instance['region']}")
        print("-" * 50)
