from app.agents.base_agent import BaseAgent


class CostAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Cost Agent"
        )

    def run(self, context):

        monthly_cost = context.get(
            "monthly_cost"
        )

        if monthly_cost is None:

            return {
                "agent": self.name,
                "status": "NO_DATA",
                "reason": "No cost data available"
            }

        monthly_cost = float(
            monthly_cost
        )

        if monthly_cost >= 100:

            cost_level = "HIGH"

        elif monthly_cost >= 50:

            cost_level = "MEDIUM"

        else:

            cost_level = "LOW"

        return {

            "agent": self.name,

            "monthly_cost": round(
                monthly_cost,
                2
            ),

            "cost_level": cost_level
        }
