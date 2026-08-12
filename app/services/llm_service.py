from app.agents.llm_agent import LLMAgent


# ============================================================
# LLM AGENT
# ============================================================

llm_agent = LLMAgent()


# ============================================================
# GENERATE SINGLE RECOMMENDATION
# ============================================================

def generate_llm_recommendation(
    decision
):
    """
    Generate a natural-language cloud
    optimization recommendation using
    the local Ollama LLM.
    """

    resource_id = decision.get(
        "resource_id"
    )

    context = {

        "resource_id":
            resource_id,

        "instance_type":
            decision.get(
                "instance_type"
            ),

        "region":
            decision.get(
                "region"
            ),

        "state":
            decision.get(
                "state"
            ),

        "cpu_status":
            decision.get(
                "cpu_status"
            ),

        "average_cpu":
            decision.get(
                "average_cpu"
            ),

        "metric_samples":
            decision.get(
                "metric_samples"
            ),

        "monthly_cost":
            decision.get(
                "monthly_cost"
            ),

        "cost_source":
            decision.get(
                "cost_source"
            ),

        "recommendation":
            decision.get(
                "recommendation"
            ),

        "priority":
            decision.get(
                "priority"
            ),

        "estimated_savings":
            decision.get(
                "estimated_savings"
            ),

        "risk_level":
            decision.get(
                "risk_level"
            ),

        "final_decision":
            decision.get(
                "final_decision"
            ),

        "execution_allowed":
            decision.get(
                "execution_allowed"
            ),

        "reason":
            decision.get(
                "risk_reason"
            )
    }

    return llm_agent.run(
        context
    )


# ============================================================
# GENERATE RECOMMENDATIONS FOR ALL
# ============================================================

def generate_llm_recommendations(
    decisions
):
    """
    Generate LLM recommendations for
    every resource decision.
    """

    results = []

    print(
        "\n========================================"
    )

    print(
        "       OLLAMA AI RECOMMENDATIONS"
    )

    print(
        "========================================"
    )

    for decision in decisions:

        resource_id = decision.get(
            "resource_id"
        )

        print(
            f"\nGenerating AI recommendation "
            f"for {resource_id}..."
        )

        try:

            recommendation = (
                generate_llm_recommendation(
                    decision
                )
            )

            results.append({

                "resource_id":
                    resource_id,

                "decision":
                    decision,

                "llm_recommendation":
                    recommendation
            })

            print(
                "✓ AI recommendation generated"
            )

        except Exception as error:

            print(
                "✗ LLM recommendation failed:"
            )

            print(error)

            results.append({

                "resource_id":
                    resource_id,

                "decision":
                    decision,

                "llm_recommendation":
                    None,

                "error":
                    str(error)
            })

    return results
