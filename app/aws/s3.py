import boto3


def get_s3_buckets():
    """
    Retrieve S3 bucket information.
    """

    s3 = boto3.client("s3")

    response = s3.list_buckets()

    buckets = []

    for bucket in response.get("Buckets", []):

        bucket_data = {
            "name": bucket["Name"],
            "creation_date": str(bucket["CreationDate"])
        }

        buckets.append(bucket_data)

    return buckets
