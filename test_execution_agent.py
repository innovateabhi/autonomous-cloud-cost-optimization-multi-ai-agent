from app.agents.execution_agent import (
    ExecutionAgent
)

agent = ExecutionAgent()


# ----------------------------------------
# TEST 1
# ----------------------------------------

result = agent.run({

    "resource": {

        "resource_id":
            "i-test123"
    },

    "optimization": {

        "recommendation":
            "RIGHTSIZE_EC2"
    },

    "risk": {

        "decision":
            "REVIEW"
    }
})

print("\nTEST 1")
print(result)


# ----------------------------------------
# TEST 2
# ----------------------------------------

result = agent.run({

    "resource": {

        "resource_id":
            "i-test456"
    },

    "optimization": {

        "recommendation":
            "NO_RECOMMENDATION"
    },

    "risk": {

        "decision":
            "DO_NOTHING"
    }
})

print("\nTEST 2")
print(result)
