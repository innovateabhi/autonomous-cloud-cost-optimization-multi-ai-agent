from app.agents.risk_agent import RiskAgent


risk_agent = RiskAgent()


def evaluate_risk(
    analysis_result
):
    """
    Evaluate the risk of an optimization
    recommendation.
    """

    if not analysis_result:

        return {
            "status": "NO_DATA",
            "reason": "No analysis result available."
        }

    resource = analysis_result.get(
        "resource",
        {}
    )

    optimization = analysis_result.get(
        "optimization",
        {}
    )

    context = {

        "resource":
            resource,

        "optimization":
            optimization
    }

    return risk_agent.run(
        context
    )


def evaluate_all_risks(
    analysis_results
):
    """
    Evaluate risk for every analyzed resource.
    """

    results = []

    for analysis_result in analysis_results:

        try:

            risk_result = evaluate_risk(
                analysis_result
            )

            results.append({

                "resource":
                    analysis_result.get(
                        "resource",
                        {}
                    ),

                "optimization":
                    analysis_result.get(
                        "optimization",
                        {}
                    ),

                "risk":
                    risk_result
            })

        except Exception as error:

            results.append({

                "resource":
                    analysis_result.get(
                        "resource",
                        {}
                    ),

                "optimization":
                    analysis_result.get(
                        "optimization",
                        {}
                    ),

                "risk": {

                    "status":
                        "ERROR",

                    "reason":
                        str(error)
                }
            })

    return results
