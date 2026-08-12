from app.agents.base_agent import BaseAgent


class ExecutionAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Execution Agent"
        )

    def run(self, context):

        resource = context.get(
            "resource",
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

        recommendation = optimization.get(
            "recommendation"
        )

        decision = risk.get(
            "decision"
        )

        resource_id = resource.get(
            "resource_id"
        )

        # ----------------------------------
        # NO ACTION
        # ----------------------------------

        if recommendation in (
            "NO_ACTION",
            "NO_RECOMMENDATION"
        ):

            return {

                "agent": self.name,

                "resource_id":
                    resource_id,

                "action":
                    "NONE",

                "status":
                    "BLOCKED",

                "reason":
                    "No optimization action available."
            }

        # ----------------------------------
        # REVIEW REQUIRED
        # ----------------------------------

        if decision == "REVIEW":

            return {

                "agent": self.name,

                "resource_id":
                    resource_id,

                "action":
                    recommendation,

                "status":
                    "BLOCKED",

                "reason":
                    "Human approval required."
            }

        # ----------------------------------
        # DRY RUN EXECUTION
        # ----------------------------------

        if decision == "APPROVE":

            return {

                "agent": self.name,

                "resource_id":
                    resource_id,

                "action":
                    recommendation,

                "status":
                    "DRY_RUN",

                "reason":
                    "Action would be executed."
            }

        return {

            "agent": self.name,

            "resource_id":
                resource_id,

            "action":
                recommendation,

            "status":
                "BLOCKED",

            "reason":
                "Execution denied."
        }
