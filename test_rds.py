from app.aws.rds import get_rds_instances


databases = get_rds_instances()


if not databases:
    print("No RDS instances found.")

else:

    print("RDS DATABASES")
    print("=" * 50)

    for database in databases:

        print(f"Identifier       : {database['identifier']}")
        print(f"Engine           : {database['engine']}")
        print(f"Instance Class   : {database['instance_class']}")
        print(f"Status           : {database['status']}")
        print(f"Storage          : {database['storage_gb']} GB")
        print(f"Multi-AZ         : {database['multi_az']}")

        print("-" * 50)
