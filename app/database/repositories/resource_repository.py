from sqlalchemy import select

from app.database.models import Resource


def create_resource(session, resource_data):

    resource = Resource(
        resource_id=resource_data["resource_id"],
        resource_type=resource_data["resource_type"],
        name=resource_data.get("name"),
        region=resource_data["region"],
        state=resource_data.get("state"),
        instance_type=resource_data.get("instance_type"),
        environment=resource_data.get("environment"),
        tags=resource_data.get("tags")
    )

    session.add(resource)

    session.commit()

    session.refresh(resource)

    return resource


def get_resource_by_id(
    session,
    resource_id
):

    statement = select(Resource).where(
        Resource.resource_id == resource_id
    )

    return session.execute(
        statement
    ).scalar_one_or_none()


def get_all_resources(session):

    statement = select(Resource)

    return session.execute(
        statement
    ).scalars().all()


def delete_resource(
    session,
    resource_id
):

    resource = get_resource_by_id(
        session,
        resource_id
    )

    if resource is None:
        return False

    session.delete(resource)

    session.commit()

    return True
