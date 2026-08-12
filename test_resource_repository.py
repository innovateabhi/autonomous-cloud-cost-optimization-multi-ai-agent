from app.database.session import SessionLocal

from app.database.repositories.resource_repository import (
    create_resource,
    get_resource_by_id,
    get_all_resources,
    delete_resource
)


session = SessionLocal()


try:

    # --------------------------------
    # CREATE
    # --------------------------------

    resource_data = {

        "resource_id": "repo-test-001",

        "resource_type": "EC2",

        "name": "Repository Test",

        "region": "ap-south-2",

        "state": "running",

        "instance_type": "t3.micro",

        "environment": "development",

        "tags": {
            "Project": "CloudOptimizer",
            "Test": "Repository"
        }
    }


    resource = create_resource(
        session,
        resource_data
    )


    print(
        "✓ Resource created:"
    )

    print(
        resource.resource_id
    )


    # --------------------------------
    # READ ONE
    # --------------------------------

    found_resource = get_resource_by_id(
        session,
        "repo-test-001"
    )


    print(
        "\n✓ Resource retrieved:"
    )

    print(
        found_resource.name
    )


    # --------------------------------
    # READ ALL
    # --------------------------------

    resources = get_all_resources(
        session
    )


    print(
        "\n✓ Total resources:"
    )

    print(
        len(resources)
    )


    # --------------------------------
    # DELETE
    # --------------------------------

    deleted = delete_resource(
        session,
        "repo-test-001"
    )


    print(
        "\n✓ Resource deleted:"
    )

    print(
        deleted
    )


finally:

    session.close()
