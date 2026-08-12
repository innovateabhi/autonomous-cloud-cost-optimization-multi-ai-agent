from app.agents.decision_agent import DecisionAgent


agent = DecisionAgent()


print("\n========================================")
print("       DECISION AGENT TEST")
print("========================================")


# ==========================================
# TEST 1
# UNDERUTILIZED + LOW RISK
# ==========================================

context_1 = {

    "resource": {
        "resource_id":
            "i-test-underutilized"
    },

    "utilization": {
        "status":
            "UNDERUTILIZED"
    },

    "optimization": {
        "recommendation":
            "RIGHTSIZE_EC2",
        "priority":
            "HIGH"
    },

    "risk": {
        "risk_level":
            "LOW",
        "decision":
            "REVIEW"
    },

    "cost": {
        "monthly_cost":
            7.59
    }
}


result_1 = agent.run(
    context_1
)

print("\nTEST 1: UNDERUTILIZED")
print(
    f"Decision: "
    f"{result_1['decision']}"
)

print(
    f"Execution Allowed: "
    f"{result_1['execution_allowed']}"
)

print(
    f"Reason: "
    f"{result_1['reason']}"
)


# ==========================================
# TEST 2
# HIGH RISK
# ==========================================

context_2 = {

    "resource": {
        "resource_id":
            "i-test-high-risk"
    },

    "utilization": {
        "status":
            "HIGH_UTILIZATION"
    },

    "optimization": {
        "recommendation":
            "RIGHTSIZE_EC2",
        "priority":
            "HIGH"
    },

    "risk": {
        "risk_level":
            "HIGH",
        "decision":
            "REVIEW"
    },

    "cost": {
        "monthly_cost":
            7.59
    }
}


result_2 = agent.run(
    context_2
)

print("\nTEST 2: HIGH RISK")
print(
    f"Decision: "
    f"{result_2['decision']}"
)

print(
    f"Execution Allowed: "
    f"{result_2['execution_allowed']}"
)

print(
    f"Reason: "
    f"{result_2['reason']}"
)


# ==========================================
# TEST 3
# NO DATA
# ==========================================

context_3 = {

    "resource": {
        "resource_id":
            "i-test-no-data"
    },

    "utilization": {
        "status":
            "NO_DATA"
    },

    "optimization": {
        "recommendation":
            "NO_RECOMMENDATION",
        "priority":
            "LOW"
    },

    "risk": {
        "risk_level":
            "LOW",
        "decision":
            "DO_NOTHING"
    },

    "cost": {
        "monthly_cost":
            7.59
    }
}


result_3 = agent.run(
    context_3
)

print("\nTEST 3: NO DATA")
print(
    f"Decision: "
    f"{result_3['decision']}"
)

print(
    f"Execution Allowed: "
    f"{result_3['execution_allowed']}"
)

print(
    f"Reason: "
    f"{result_3['reason']}"
)


print("\n========================================")
print("       TEST COMPLETED")
print("========================================")
