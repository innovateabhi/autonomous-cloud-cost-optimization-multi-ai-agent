from app.agents.llm_agent import LLMAgent


def main():

    print("\n========================================")
    print("       LOCAL LLM AGENT TEST")
    print("========================================\n")

    # Create LLM agent
    agent = LLMAgent()

    # Sample data coming from our other AI agents
    context = {

        "resource": {

            "resource_id":
                "i-demo123456",

            "resource_type":
                "EC2",

            "instance_type":
                "t3.large",

            "region":
                "ap-south-2",

            "state":
                "running",

            "environment":
                "development"
        },

        "utilization": {

            "status":
                "UNDERUTILIZED",

            "average_cpu":
                6.36,

            "minimum_cpu":
                4.9,

            "maximum_cpu":
                8.2,

            "samples":
                5
        },

        "cost": {

            "monthly_cost":
                82,

            "cost_level":
                "MEDIUM"
        },

        "optimization": {

            "recommendation":
                "RIGHTSIZE_EC2",

            "priority":
                "HIGH",

            "estimated_savings":
                24.60
        },

        "risk": {

            "risk_level":
                "LOW",

            "approval":
                "APPROVED",

            "risk_factors":
                []
        }
    }

    print("Sending structured data to LLM...\n")

    try:

        result = agent.run(
            context
        )

        print("========== LLM RESULT ==========\n")

        print(
            f"Agent: "
            f"{result.get('agent')}"
        )

        print(
            f"Model: "
            f"{result.get('model')}"
        )

        print(
            f"Status: "
            f"{result.get('status')}"
        )

        print(
            "\n========== RECOMMENDATION ==========\n"
        )

        print(
            result.get(
                "recommendation",
                "No recommendation returned."
            )
        )

        print(
            "\n========================================"
        )

    except Exception as error:

        print(
            "\n========== LLM ERROR ==========\n"
        )

        print(error)

        print(
            "\n========================================"
        )


if __name__ == "__main__":

    main()
