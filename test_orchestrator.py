from app.agents.orchestrator import AgentOrchestrator


def main():

    print("\n")
    print("========================================")
    print("     MULTI-AGENT SYSTEM TEST")
    print("========================================")

    # --------------------------------------------------
    # TEST RESOURCE
    # --------------------------------------------------

    resource = {

        "resource_id":
            "i-demo123456",

        "resource_type":
            "EC2",

        "name":
            "demo-server",

        "region":
            "ap-south-2",

        "state":
            "running",

        "instance_type":
            "t3.large",

        "environment":
            "development",

        "tags": {

            "Name":
                "demo-server",

            "Environment":
                "development"
        }
    }

    # --------------------------------------------------
    # CREATE ORCHESTRATOR
    # --------------------------------------------------

    orchestrator = AgentOrchestrator()

    # --------------------------------------------------
    # RUN COMPLETE PIPELINE
    # --------------------------------------------------

    try:

        result = orchestrator.run(
            resource
        )

        # --------------------------------------------------
        # DISPLAY RESULTS
        # --------------------------------------------------

        print("\n")
        print("========================================")
        print("           FINAL RESULTS")
        print("========================================")

        print("\n--- RESOURCE ---")

        print(
            result.get(
                "resource"
            )
        )

        print("\n--- UTILIZATION ---")

        print(
            result.get(
                "utilization"
            )
        )

        print("\n--- COST ---")

        print(
            result.get(
                "cost"
            )
        )

        print("\n--- OPTIMIZATION ---")

        print(
            result.get(
                "optimization"
            )
        )

        print("\n--- RISK ---")

        print(
            result.get(
                "risk"
            )
        )

        print("\n--- LLM RECOMMENDATION ---")

        llm_result = result.get(
            "llm",
            {}
        )

        print(
            llm_result.get(
                "recommendation",
                "No recommendation available."
            )
        )

        print("\n")
        print("========================================")
        print("       TEST COMPLETED SUCCESSFULLY")
        print("========================================")

    except Exception as error:

        print("\n")
        print("========================================")
        print("              ERROR")
        print("========================================")

        print(error)


if __name__ == "__main__":

    main()
