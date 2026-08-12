from app.services.analysis_service import (
    analyze_all_resources
)


# ============================================================
# BUILD FINAL DECISION
# ============================================================

def build_decision(analysis):
    """
    Convert the multi-agent analysis result into
    a clean final decision.
    """

    resource = analysis.get(
        "resource",
        {}
    )

    utilization = analysis.get(
        "utilization",
        {}
    )

    cost = analysis.get(
        "cost",
        {}
    )

    optimization = analysis.get(
        "optimization",
        {}
    )

    risk = analysis.get(
        "risk",
        {}
    )

    resource_id = resource.get(
        "resource_id"
    )

    recommendation = optimization.get(
        "recommendation",
        "NO_RECOMMENDATION"
    )

    priority = optimization.get(
        "priority",
        "LOW"
    )

    estimated_savings = optimization.get(
        "estimated_savings",
        0
    )

    monthly_cost = cost.get(
        "monthly_cost"
    )

    cost_source = cost.get(
        "cost_source",
        "UNKNOWN"
    )

    cpu_status = utilization.get(
        "status"
    )

    average_cpu = utilization.get(
        "average_cpu"
    )

    samples = utilization.get(
        "samples",
        0
    )

    risk_level = risk.get(
        "risk_level",
        "UNKNOWN"
    )

    risk_decision = risk.get(
        "decision",
        "REVIEW"
    )

    risk_reason = risk.get(
        "reason",
        "No reason provided."
    )

    # ========================================================
    # FINAL DECISION LOGIC
    # ========================================================

    if recommendation in (
        "NO_ACTION",
        "NO_RECOMMENDATION"
    ):

        final_decision = "DO_NOTHING"

        execution_allowed = False

    elif risk_decision == "DO_NOTHING":

        final_decision = "DO_NOTHING"

        execution_allowed = False

    elif risk_level == "HIGH":

        final_decision = "REVIEW"

        execution_allowed = False

    elif risk_decision == "REVIEW":

        final_decision = "REVIEW"

        execution_allowed = False

    else:

        final_decision = "REVIEW"

        execution_allowed = False

    # ========================================================
    # RETURN FINAL RESULT
    # ========================================================

    return {

        "resource_id":
            resource_id,

        "resource_type":
            resource.get(
                "resource_type"
            ),

        "instance_type":
            resource.get(
                "instance_type"
            ),

        "region":
            resource.get(
                "region"
            ),

        "state":
            resource.get(
                "state"
            ),

        "cpu_status":
            cpu_status,

        "average_cpu":
            average_cpu,

        "metric_samples":
            samples,

        "monthly_cost":
            monthly_cost,

        "cost_source":
            cost_source,

        "cost_level":
            cost.get(
                "cost_level"
            ),

        "recommendation":
            recommendation,

        "priority":
            priority,

        "estimated_savings":
            estimated_savings,

        "risk_level":
            risk_level,

        "risk_decision":
            risk_decision,

        "risk_reason":
            risk_reason,

        "final_decision":
            final_decision,

        "execution_allowed":
            execution_allowed
    }


# ============================================================
# ANALYZE AND DECIDE
# ============================================================

def generate_decisions(
    hours=24
):
    """
    Run the complete multi-agent analysis
    and generate final decisions for all
    resources.
    """

    print(
        "\n========================================"
    )

    print(
        "       FINAL DECISION ENGINE"
    )

    print(
        "========================================"
    )

    # ========================================================
    # RUN ANALYSIS PIPELINE
    # ========================================================

    analysis_results = (
        analyze_all_resources(
            hours=hours
        )
    )

    decisions = []

    # ========================================================
    # BUILD FINAL DECISIONS
    # ========================================================

    for analysis in analysis_results:

        if analysis.get("error"):

            decisions.append({

                "resource_id":
                    analysis
                    .get("resource", {})
                    .get("resource_id"),

                "final_decision":
                    "ERROR",

                "execution_allowed":
                    False,

                "error":
                    analysis.get(
                        "error"
                    )
            })

            continue

        decision = build_decision(
            analysis
        )

        decisions.append(
            decision
        )

    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    print(
        "\n========================================"
    )

    print(
        "       DECISION SUMMARY"
    )

    print(
        "========================================"
    )

    for decision in decisions:

        print(
            "\n----------------------------------------"
        )

        print(
            f"Resource: "
            f"{decision.get('resource_id')}"
        )

        print(
            f"CPU Status: "
            f"{decision.get('cpu_status')}"
        )

        print(
            f"Average CPU: "
            f"{decision.get('average_cpu')}"
        )

        print(
            f"Monthly Cost: "
            f"${decision.get('monthly_cost')}"
        )

        print(
            f"Recommendation: "
            f"{decision.get('recommendation')}"
        )

        print(
            f"Priority: "
            f"{decision.get('priority')}"
        )

        print(
            f"Estimated Savings: "
            f"${decision.get('estimated_savings')}"
        )

        print(
            f"Risk Level: "
            f"{decision.get('risk_level')}"
        )

        print(
            f"Final Decision: "
            f"{decision.get('final_decision')}"
        )

        print(
            f"Execution Allowed: "
            f"{decision.get('execution_allowed')}"
        )

        print(
            f"Reason: "
            f"{decision.get('risk_reason')}"
        )

    return decisions
