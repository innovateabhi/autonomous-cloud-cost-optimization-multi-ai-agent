from app.database.models import AuditLog, Resource


def create_audit_log(
    session,
    audit_data
):
    """
    Create a new audit log entry.

    The incoming resource_id may be an AWS resource ID
    such as i-0e6178ff13b9b326b.

    The audit_logs table stores the internal integer
    resources.id as its foreign key.
    """

    aws_resource_id = audit_data.get(
        "resource_id"
    )

    internal_resource_id = None

    # --------------------------------------------------
    # Resolve AWS resource ID -> internal database ID
    # --------------------------------------------------

    if aws_resource_id:

        resource = session.query(
            Resource
        ).filter(
            Resource.resource_id == aws_resource_id
        ).first()

        if resource:

            internal_resource_id = resource.id

    # --------------------------------------------------
    # Create audit log
    # --------------------------------------------------

    audit = AuditLog(

        resource_id=
            internal_resource_id,

        recommendation_id=
            audit_data.get(
                "recommendation_id"
            ),

        action_id=
            audit_data.get(
                "action_id"
            ),

        event_type=
            audit_data.get(
                "event_type",
                "ANALYSIS"
            ),

        agent_name=
            audit_data.get(
                "agent_name"
            ),

        recommendation=
            audit_data.get(
                "recommendation"
            ),

        priority=
            audit_data.get(
                "priority"
            ),

        risk_level=
            audit_data.get(
                "risk_level"
            ),

        decision=
            audit_data.get(
                "decision"
            ),

        execution_action=
            audit_data.get(
                "execution_action"
            ),

        execution_status=
            audit_data.get(
                "execution_status"
            ),

        estimated_savings=
            audit_data.get(
                "estimated_savings"
            ),

        llm_status=
            audit_data.get(
                "llm_status"
            ),

        llm_model=
            audit_data.get(
                "llm_model"
            ),

        llm_recommendation=
            audit_data.get(
                "llm_recommendation"
            ),

        confidence=
            audit_data.get(
                "confidence"
            ),

        status=
            audit_data.get(
                "status"
            ),

        message=
            audit_data.get(
                "message"
            )
    )

    session.add(audit)

    session.commit()

    session.refresh(audit)

    return audit
