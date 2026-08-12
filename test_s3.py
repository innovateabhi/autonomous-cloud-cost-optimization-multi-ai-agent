from app.aws.s3 import get_s3_buckets


buckets = get_s3_buckets()


if not buckets:
    print("No S3 buckets found.")

else:

    print("S3 BUCKETS")
    print("=" * 50)

    for bucket in buckets:

        print(f"Bucket Name    : {bucket['name']}")
        print(f"Creation Date  : {bucket['creation_date']}")

        print("-" * 50)
