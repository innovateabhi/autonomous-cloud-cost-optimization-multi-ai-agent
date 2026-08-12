from sqlalchemy import select

from app.database.models import Action


def create_action(
    session,
    action_data
):

    action = Action(

        recommendation_id=(
            action_data[
                "recommendation_id"
            ]
        ),

        action_type=(
            action_data[
                "action_type"
            ]
        ),

        status=(
            action_data.get(
                "status"
            )
        ),

        result=(
            action_data.get(
                "result"
            )
        ),

        error_message=(
            action_data.get(
                "error_message"
            )
        ),

        approved_by=(
            action_data.get(
                "approved_by"
            )
        )
    )

    session.add(action)

    session.commit()

    session.refresh(action)

    return action


def get_actions_for_recommendation(
    session,
    recommendation_id
):

    statement = (
        select(Action)
        .where(
            Action.recommendation_id
            == recommendation_id
        )
        .order_by(
            Action.executed_at
        )
    )

    return session.execute(
        statement
    ).scalars().all()
