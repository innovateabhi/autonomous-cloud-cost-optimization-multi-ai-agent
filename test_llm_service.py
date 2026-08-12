from app.services.analysis_service import (
    analyze_all_resources
)

from app.services.risk_service import (
    evaluate_all_risks
)

from app.services.llm_service import (
    generate_llm_recommendations
)


print("\n========================================")
print("       LLM SERVICE TEST")
print("========================================\n")


# ------------------------------------------
# STEP 1: ANALYSIS
# ------------------------------------------

print("Running analysis...\n")

analysis_results = analyze_all_resources(
    hours=24
)


# ------------------------------------------
# STEP 2: RISK
# ------------------------------------------

print("\nRunning risk evaluation...\n")

risk_results = evaluate_all_risks(
    analysis_results
)


# ------------------------------------------
# STEP 3: LLM
# ------------------------------------------

print("\nRunning Ollama LLM...\n")

llm_results = generate_llm_recommendations(

    analysis_results=
        analysis_results,

    risk_results=
        risk_results
)


# ------------------------------------------
# DISPLAY
# ------------------------------------------

print("\n========================================")
print("       FINAL AI RESULTS")
print("========================================\n")


for result in llm_results:

    resource = result.get(
        "resource",
        {}
    )

    llm = result.get(
        "llm",
        {}
    )

    print("----------------------------------------")

    print(
        f"Resource: "
        f"{resource.get('resource_id')}"
    )

    print(
        f"Instance Type: "
        f"{resource.get('instance_type')}"
    )

    print(
        f"LLM Status: "
        f"{llm.get('status')}"
    )

    print("\nAI Recommendation:")

    print(
        llm.get(
            "recommendation",
            "No recommendation generated."
        )
    )

    print()


print("========================================")
print("       TEST COMPLETED")
print("========================================")
