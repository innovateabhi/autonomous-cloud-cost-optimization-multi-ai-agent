from statistics import mean

from app.agents.base_agent import BaseAgent


class UtilizationAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Utilization Agent"
        )

    def run(self, context):

        cpu_values = context.get(
            "cpu_values",
            []
        )

        if not cpu_values:

            return {
                "agent": self.name,
                "status": "NO_DATA",
                "reason": "No CPU metrics available"
            }

        cpu_values = [
            float(value)
            for value in cpu_values
        ]

        average_cpu = mean(cpu_values)

        minimum_cpu = min(
            cpu_values
        )

        maximum_cpu = max(
            cpu_values
        )

        if average_cpu < 10:

            status = "UNDERUTILIZED"

        elif average_cpu < 40:

            status = "LOW_UTILIZATION"

        elif average_cpu < 70:

            status = "NORMAL"

        else:

            status = "HIGH_UTILIZATION"

        return {

            "agent": self.name,

            "status": status,

            "average_cpu": round(
                average_cpu,
                2
            ),

            "minimum_cpu": round(
                minimum_cpu,
                2
            ),

            "maximum_cpu": round(
                maximum_cpu,
                2
            ),

            "samples": len(
                cpu_values
            )
        }
