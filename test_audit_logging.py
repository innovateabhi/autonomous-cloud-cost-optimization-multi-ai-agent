from app.database.session import SessionLocal

from app.services.audit_service import (
    log_analysis_result
)


print("\n========================================")
print("       AUDIT LOGGING TEST")
print("========================================\n")


test_result = {

    "resource": {

        "resource_id":
            "i-test123"
    },

    "optimization": {

        "recommendation":
            "RIGHTSIZE_EC2",

        "priority":
            "HIGH",

        "estimated_savings":
            2.28
    },

    "risk": {

        "risk_level":
            "MEDIUM",

        "decision":
            "REVIEW"
    },

    "execution": {

        "action":
            "RIGHTSIZE_EC2",

        "status":
            "BLOCKED"
    },

    "llm": {

        "status":
            "COMPLETED",

        "model":
            "qwen3:1.7b",

        "recommendation":
            "Human approval required."
    }
}


audit = log_analysis_result(
    test_result
)


print(
    f"Audit ID: {audit.id}"
)

print(
    f"Resource: {audit.resource_id}"
)

print(
    f"Recommendation: "
    f"{audit.recommendation}"
)

print(
    f"Risk: {audit.risk_level}"
)

print(
    f"Decision: {audit.decision}"
)

print(
    f"Execution: "
    f"{audit.execution_status}"
)

print(
    f"Savings: "
    f"${audit.estimated_savings:.2f}"
)

print(
    f"LLM Model: "
    f"{audit.llm_model}"
)

print(
    f"Created: "
    f"{audit.created_at}"
)

print("\n✓ Audit logging test completed.")
