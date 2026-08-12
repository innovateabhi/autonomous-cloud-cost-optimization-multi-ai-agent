from app.agents.base_agent import BaseAgent


class DecisionAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            "Optimization Decision Agent"
        )

    def run(self, context):

        resource = context.get(
            "resource",
            {}
        )

        utilization = context.get(
            "utilization",
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

        cost = context.get(
            "cost",
            {}
        )

        resource_id = resource.get(
            "resource_id"
        )

        recommendation = optimization.get(
            "recommendation"
        )

        priority = optimization.get(
            "priority"
        )

        risk_level = risk.get(
            "risk_level"
        )

        risk_decision = risk.get(
            "decision"
        )

        cpu_status = utilization.get(
            "status"
        )

        monthly_cost = cost.get(
            "monthly_cost"
        )

        # ==========================================
        # NO RECOMMENDATION
        # ==========================================

        if recommendation in (
            None,
            "NO_ACTION",
            "NO_RECOMMENDATION"
        ):

            return {
                "agent": self.name,
                "resource_id": resource_id,
                "decision": "DO_NOTHING",
                "execution_allowed": False,
                "reason":
                    "No optimization "
                    "recommendation is available."
            }

        # ==========================================
        # NO DATA
        # ==========================================

        if cpu_status == "NO_DATA":

            return {
                "agent": self.name,
                "resource_id": resource_id,
                "decision": "DO_NOTHING",
                "execution_allowed": False,
                "reason":
                    "Insufficient monitoring "
                    "data for safe optimization."
            }

        # ==========================================
        # HIGH RISK
        # ==========================================

        if risk_level == "HIGH":

            return {
                "agent": self.name,
                "resource_id": resource_id,
                "decision": "MANUAL_REVIEW",
                "execution_allowed": False,
                "reason":
                    "Optimization has been classified "
                    "as high risk."
            }

        # ==========================================
        # RISK AGENT SAYS DO NOTHING
        # ==========================================

        if risk_decision == "DO_NOTHING":

            return {
                "agent": self.name,
                "resource_id": resource_id,
                "decision": "DO_NOTHING",
                "execution_allowed": False,
                "reason":
                    "Risk evaluation recommends "
                    "no action."
            }

        # ==========================================
        # LOW RISK + RIGHTSIZING
        # ==========================================

        if (
            recommendation == "RIGHTSIZE_EC2"
            and risk_level == "LOW"
            and risk_decision == "REVIEW"
        ):

            return {
                "agent": self.name,
                "resource_id": resource_id,
                "decision": "APPROVE_RIGHTSIZING",
                "execution_allowed": False,
                "reason":
                    "Resource is underutilized and "
                    "risk is low. Rightsizing is "
                    "approved for review but automatic "
                    "execution remains disabled.",
                "priority": priority,
                "monthly_cost": monthly_cost
            }

        # ==========================================
        # MEDIUM RISK
        # ==========================================

        if risk_level == "MEDIUM":

            return {
                "agent": self.name,
                "resource_id": resource_id,
                "decision": "MANUAL_REVIEW",
                "execution_allowed": False,
                "reason":
                    "Optimization requires "
                    "manual review because "
                    "risk is medium.",
                "priority": priority
            }

        # ==========================================
        # DEFAULT
        # ==========================================

        return {
            "agent": self.name,
            "resource_id": resource_id,
            "decision": "MANUAL_REVIEW",
            "execution_allowed": False,
            "reason":
                "Optimization recommendation "
                "requires manual review.",
            "priority": priority
        }
