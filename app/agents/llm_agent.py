import json
import requests

from app.agents.base_agent import BaseAgent
from app.config import (
    OLLAMA_HOST,
    OLLAMA_MODEL
)


class LLMAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "LLM Recommendation Agent"
        )

        self.ollama_host = OLLAMA_HOST
        self.model = OLLAMA_MODEL

    # ==================================================
    # BUILD PROMPT
    # ==================================================

    def build_prompt(self, context):

        resource = context.get(
            "resource",
            {}
        )

        utilization = context.get(
            "utilization",
            {}
        )

        cost = context.get(
            "cost",
            {}
        )

        optimization = context.get(
            "optimization",
            {}
        )

        risk = context.get(
            "risk",
            {}
        )

        decision = context.get(
            "decision",
            {}
        )

        evidence = {

            "resource": resource,

            "utilization": utilization,

            "cost": cost,

            "optimization": optimization,

            "risk": risk,

            "decision": decision
        }

        return f"""
You are an expert cloud cost optimization analyst.

You are part of an autonomous cloud cost
optimization system.

Your job is to explain the decision already
made by the deterministic decision engine.

IMPORTANT:

Analyze ONLY the structured evidence below.

Do NOT invent:

- AWS metrics
- AWS prices
- resource information
- savings
- utilization values
- recommendations
- risk levels

If a value is missing, explicitly say
that the value is unavailable.

STRUCTURED EVIDENCE:

{json.dumps(
    evidence,
    indent=2,
    default=str
)}

--------------------------------------------------
ANALYSIS RULES
--------------------------------------------------

1. Respect the Optimization Agent.

2. Respect the Risk Agent.

3. Respect the Final Decision.

4. Never override the Risk Agent.

5. Never recommend automatic execution if
   execution is not allowed.

6. Do not invent savings.

7. Do not invent AWS pricing.

8. Do not claim that metrics are missing when
   they are present in the structured evidence.

9. If the final decision is REVIEW, clearly
   state that human approval is required.

10. If the final decision is DO_NOTHING,
    clearly state that no optimization action
    should currently be performed.

--------------------------------------------------
REQUIRED RESPONSE FORMAT
--------------------------------------------------

1. Current Situation

Describe the actual resource and its
utilization.

2. Detected Optimization Opportunity

Explain the recommendation from the
Optimization Agent.

3. Reasoning

Explain why the optimization was suggested,
using only the supplied evidence.

4. Estimated Savings

Report the supplied estimated savings.

Do not calculate a new value.

5. Risk Assessment

Report the Risk Agent's risk level and
reason.

6. Recommended Action

Follow the Final Decision.

7. Human Approval Requirement

Clearly state whether human approval is
required.

Keep the response concise and factual.
"""


    # ==================================================
    # RUN OLLAMA
    # ==================================================

    def run(self, context):

        prompt = self.build_prompt(
            context
        )

        url = (
            f"{self.ollama_host}"
            "/api/chat"
        )

        payload = {

            "model":
                self.model,

            "messages": [

                {
                    "role":
                        "system",

                    "content":
                        (
                            "You are a conservative "
                            "cloud cost optimization "
                            "analyst. Never invent "
                            "cloud infrastructure "
                            "data."
                        )
                },

                {
                    "role":
                        "user",

                    "content":
                        prompt
                }

            ],

            "stream":
                False,

            "options": {

                "temperature":
                    0.1
            }
        }

        try:

            response = requests.post(

                url,

                json=payload,

                timeout=300
            )

            response.raise_for_status()

            data = response.json()

            recommendation = (
                data
                .get("message", {})
                .get("content", "")
            )

            if not recommendation:

                raise ValueError(
                    "Ollama returned an empty response."
                )

            return {

                "agent":
                    self.name,

                "model":
                    self.model,

                "status":
                    "COMPLETED",

                "recommendation":
                    recommendation
            }

        except requests.exceptions.ConnectionError:

            raise RuntimeError(
                "Could not connect to Ollama. "
                "Make sure Ollama is running at "
                f"{self.ollama_host}."
            )

        except requests.exceptions.Timeout:

            raise RuntimeError(
                "Ollama request timed out."
            )

        except requests.exceptions.RequestException as error:

            raise RuntimeError(
                f"Ollama API request failed: {error}"
            )

        except Exception as error:

            raise RuntimeError(
                f"LLM Agent failed: {error}"
            )
