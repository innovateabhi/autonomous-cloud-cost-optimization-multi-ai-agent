from sqlalchemy import select

from app.database.models import Recommendation


def create_recommendation(
    session,
    recommendation_data
):

    recommendation = Recommendation(

        resource_id=(
            recommendation_data["resource_id"]
        ),

        recommendation_type=(
            recommendation_data[
                "recommendation_type"
            ]
        ),

        current_configuration=(
            recommendation_data.get(
                "current_configuration"
            )
        ),

        recommended_configuration=(
            recommendation_data.get(
                "recommended_configuration"
            )
        ),

        estimated_monthly_savings=(
            recommendation_data.get(
                "estimated_monthly_savings"
            )
        ),

        currency=(
            recommendation_data.get(
                "currency",
                "USD"
            )
        ),

        risk_level=(
            recommendation_data.get(
                "risk_level"
            )
        ),

        reason=(
            recommendation_data.get(
                "reason"
            )
        ),

        confidence=(
            recommendation_data.get(
                "confidence"
            )
        ),

        status=(
            recommendation_data.get(
                "status",
                "PENDING"
            )
        )
    )

    session.add(recommendation)

    session.commit()

    session.refresh(recommendation)

    return recommendation


def get_pending_recommendations(
    session
):

    statement = (
        select(Recommendation)
        .where(
            Recommendation.status == "PENDING"
        )
    )

    return session.execute(
        statement
    ).scalars().all()
