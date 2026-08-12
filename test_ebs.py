from app.aws.ebs import get_ebs_volumes


volumes = get_ebs_volumes()


if not volumes:
    print("No EBS volumes found.")

else:
    print("EBS VOLUMES")
    print("=" * 50)

    for volume in volumes:

        print(f"Volume ID          : {volume['volume_id']}")
        print(f"Volume Type        : {volume['volume_type']}")
        print(f"Size               : {volume['size_gb']} GB")
        print(f"State              : {volume['state']}")
        print(f"Attached Instance  : {volume['attached_instance']}")
        print(f"Encrypted          : {volume['encrypted']}")

        print("-" * 50)
