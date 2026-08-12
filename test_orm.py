from app.database.session import SessionLocal

from app.database.models import Resource


session = SessionLocal()


try:

    resource = Resource(

        resource_id="test-orm-001",

        resource_type="EC2",

        name="ORM Test Instance",

        region="ap-south-2",

        state="running",

        instance_type="t3.micro",

        environment="development",

        tags={
            "Project": "CloudOptimizer",
            "Environment": "Test"
        }
    )

    session.add(resource)

    session.commit()

    session.refresh(resource)

    print("Resource inserted successfully.")

    print(
        f"Database ID: {resource.id}"
    )

    print(
        f"AWS Resource ID: "
        f"{resource.resource_id}"
    )

finally:

    session.close()
