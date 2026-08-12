from app.services.analysis_service import (
    analyze_all_resources
)

from app.agents.llm_agent import (
    LLMAgent
)


# ==================================================
# CONFIGURATION
# ==================================================

ANALYSIS_HOURS = 24


# ==================================================
# HEADER
# ==================================================

print("\n========================================")
print("       LLM CLOUD OPTIMIZATION TEST")
print("========================================")


# ==================================================
# STEP 1
# RUN DECISION ENGINE
# ==================================================

print("\nStep 1: Running decision engine...\n")

results = analyze_all_resources(
    hours=ANALYSIS_HOURS
)

print("\n✓ Decision engine completed.")


# ==================================================
# CHECK RESULTS
# ==================================================

if not results:

    print(
        "\nNo resources were found."
    )

    raise SystemExit(0)


# ==================================================
# STEP 2
# INITIALIZE LLM AGENT
# ==================================================

print("\nStep 2: Initializing Ollama LLM Agent...\n")

llm_agent = LLMAgent()

print(
    f"✓ Model: {llm_agent.model}"
)

print(
    f"✓ Ollama: {llm_agent.ollama_host}"
)


# ==================================================
# STEP 3
# SEND DECISIONS TO LLM
# ==================================================

print("\nStep 3: Sending decisions to Ollama...\n")


llm_results = []


for result in results:

    resource = result.get(
        "resource",
        {}
    )

    resource_id = resource.get(
        "resource_id",
        "UNKNOWN"
    )

    print(
        f"Generating AI recommendation "
        f"for {resource_id}..."
    )

    # --------------------------------------------------
    # BUILD COMPLETE CONTEXT
    # --------------------------------------------------

    context = {

        "resource":
            result.get(
                "resource",
                {}
            ),

        "utilization":
            result.get(
                "utilization",
                {}
            ),

        "cost":
            result.get(
                "cost",
                {}
            ),

        "optimization":
            result.get(
                "optimization",
                {}
            ),

        "risk":
            result.get(
                "risk",
                {}
            )
    }

    # --------------------------------------------------
    # SEND TO LLM
    # --------------------------------------------------

    try:

        llm_result = llm_agent.run(
            context
        )

        llm_results.append({

            "resource_id":
                resource_id,

            "decision":
                result,

            "llm":
                llm_result
        })

        print(
            "✓ AI recommendation generated"
        )

    except Exception as error:

        print(
            f"✗ AI recommendation failed "
            f"for {resource_id}"
        )

        print(
            f"Error: {error}"
        )

        llm_results.append({

            "resource_id":
                resource_id,

            "decision":
                result,

            "llm": {

                "agent":
                    "LLM Recommendation Agent",

                "status":
                    "FAILED",

                "error":
                    str(error)
            }
        })


# ==================================================
# STEP 4
# DISPLAY RESULTS
# ==================================================

print("\n")
print("========================================")
print("       FINAL AI ANALYSIS")
print("========================================")


for item in llm_results:

    resource_id = item[
        "resource_id"
    ]

    decision = item[
        "decision"
    ]

    llm = item[
        "llm"
    ]

    resource = decision.get(
        "resource",
        {}
    )

    utilization = decision.get(
        "utilization",
        {}
    )

    cost = decision.get(
        "cost",
        {}
    )

    optimization = decision.get(
        "optimization",
        {}
    )

    risk = decision.get(
        "risk",
        {}
    )

    print("\n")
    print("----------------------------------------")

    print(
        f"Resource: {resource_id}"
    )

    print(
        f"Instance Type: "
        f"{resource.get('instance_type')}"
    )

    print(
        f"Region: "
        f"{resource.get('region')}"
    )

    print(
        f"CPU Status: "
        f"{utilization.get('status')}"
    )

    print(
        f"Average CPU: "
        f"{utilization.get('average_cpu')}"
    )

    print(
        f"Monthly Cost: "
        f"${cost.get('monthly_cost')}"
    )

    print(
        f"Cost Source: "
        f"{cost.get('cost_source')}"
    )

    print(
        f"Recommendation: "
        f"{optimization.get('recommendation')}"
    )

    print(
        f"Priority: "
        f"{optimization.get('priority')}"
    )

    print(
        f"Estimated Savings: "
        f"${optimization.get('estimated_savings', 0)}"
    )

    print(
        f"Risk Level: "
        f"{risk.get('risk_level')}"
    )

    print(
        f"Final Decision: "
        f"{risk.get('decision')}"
    )

    print(
        f"Execution Allowed: "
        f"{risk.get('execution_allowed', False)}"
    )

    print(
        f"\nAI Status: "
        f"{llm.get('status')}"
    )

    print(
        f"AI Model: "
        f"{llm.get('model')}"
    )

    print("\nAI Recommendation:")

    recommendation = llm.get(
        "recommendation"
    )

    if recommendation:

        print(
            recommendation
        )

    else:

        print(
            "No AI recommendation returned."
        )


# ==================================================
# SUMMARY
# ==================================================

print("\n")
print("========================================")
print("       LLM PIPELINE SUMMARY")
print("========================================")

successful = 0
failed = 0


for item in llm_results:

    status = item[
        "llm"
    ].get(
        "status"
    )

    if status == "COMPLETED":

        successful += 1

    else:

        failed += 1


print(
    f"Resources analyzed: "
    f"{len(llm_results)}"
)

print(
    f"AI recommendations generated: "
    f"{successful}"
)

print(
    f"AI failures: "
    f"{failed}"
)


print("\n✓ LLM pipeline test completed.")
print()
