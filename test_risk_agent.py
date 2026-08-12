from app.agents.risk_agent import RiskAgent


agent = RiskAgent()


print("\n========================================")
print("       RISK AGENT TEST")
print("========================================")


# --------------------------------------------------
# TEST 1: UNDERUTILIZED
# --------------------------------------------------

context = {

    "resource": {

        "resource_id":
            "i-test123",

        "state":
            "running"
    },

    "utilization": {

        "status":
            "UNDERUTILIZED",

        "average_cpu":
            0.34,

        "samples":
            22
    },

    "optimization": {

        "recommendation":
            "RIGHTSIZE_EC2",

        "priority":
            "HIGH"
    }
}


result = agent.run(context)


print("\nTEST 1: UNDERUTILIZED")

print(
    f"Risk Level: "
    f"{result['risk_level']}"
)

print(
    f"Decision: "
    f"{result['decision']}"
)

print(
    f"Reason: "
    f"{result['reason']}"
)


# --------------------------------------------------
# TEST 2: HIGH CPU
# --------------------------------------------------

context = {

    "resource": {

        "resource_id":
            "i-test456",

        "state":
            "running"
    },

    "utilization": {

        "status":
            "HIGH_UTILIZATION",

        "average_cpu":
            85.5,

        "samples":
            22
    },

    "optimization": {

        "recommendation":
            "CONSIDER_SCALING",

        "priority":
            "MEDIUM"
    }
}


result = agent.run(context)


print("\nTEST 2: HIGH UTILIZATION")

print(
    f"Risk Level: "
    f"{result['risk_level']}"
)

print(
    f"Decision: "
    f"{result['decision']}"
)

print(
    f"Reason: "
    f"{result['reason']}"
)


# --------------------------------------------------
# TEST 3: NO DATA
# --------------------------------------------------

context = {

    "resource": {

        "resource_id":
            "i-test789",

        "state":
            "running"
    },

    "utilization": {

        "status":
            "NO_DATA",

        "average_cpu":
            None,

        "samples":
            0
    },

    "optimization": {

        "recommendation":
            "NO_RECOMMENDATION",

        "priority":
            "LOW"
    }
}


result = agent.run(context)


print("\nTEST 3: NO DATA")

print(
    f"Risk Level: "
    f"{result['risk_level']}"
)

print(
    f"Decision: "
    f"{result['decision']}"
)

print(
    f"Reason: "
    f"{result['reason']}"
)


print("\n========================================")
print("       TEST COMPLETED")
print("========================================")
