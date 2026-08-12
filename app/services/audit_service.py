from app.database.session import SessionLocal

from app.database.repositories.audit_repository import (
    create_audit_log
)


def log_analysis_result(
    result
):
    """
    Store the complete decision pipeline
    result in PostgreSQL.
    """

    resource = result.get(
        "resource",
        {}
    )

    optimization = result.get(
        "optimization",
        {}
    )

    risk = result.get(
        "risk",
        {}
    )

    execution = result.get(
        "execution",
        {}
    )

    llm = result.get(
        "llm",
        {}
    )

    audit_data = {

        "resource_id":
            resource.get(
                "resource_id"
            ),

        "recommendation":
            optimization.get(
                "recommendation"
            ),

        "priority":
            optimization.get(
                "priority"
            ),

        "risk_level":
            risk.get(
                "risk_level"
            ),

        "decision":
            risk.get(
                "decision"
            ),

        "execution_action":
            execution.get(
                "action"
            ),

        "execution_status":
            execution.get(
                "status"
            ),

        "estimated_savings":
            optimization.get(
                "estimated_savings",
                0
            ),

        "llm_status":
            llm.get(
                "status"
            ),

        "llm_model":
            llm.get(
                "model"
            ),

        "llm_recommendation":
            llm.get(
                "recommendation"
            )
    }

    db = SessionLocal()

    try:

        audit = create_audit_log(
            db,
            audit_data
        )

        return audit

    finally:

        db.close()
