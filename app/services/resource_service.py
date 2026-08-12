from app.database.session import SessionLocal

from app.database.repositories.resource_repository import (
    create_resource,
    get_resource_by_id
)


def save_resource(resource_data):

    session = SessionLocal()

    try:

        existing = get_resource_by_id(
            session,
            resource_data["resource_id"]
        )

        if existing:

            existing.name = resource_data.get(
                "name"
            )

            existing.state = resource_data.get(
                "state"
            )

            existing.instance_type = (
                resource_data.get(
                    "instance_type"
                )
            )

            existing.environment = (
                resource_data.get(
                    "environment"
                )
            )

            existing.tags = resource_data.get(
                "tags"
            )

            session.commit()

            session.refresh(existing)

            return existing

        return create_resource(
            session,
            resource_data
        )

    finally:

        session.close()
