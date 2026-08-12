from app.agents.base_agent import BaseAgent


class RiskAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Risk Evaluation Agent"
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

        resource_id = resource.get(
            "resource_id"
        )

        resource_state = resource.get(
            "state"
        )

        recommendation = optimization.get(
            "recommendation"
        )

        priority = optimization.get(
            "priority"
        )

        cpu_status = utilization.get(
            "status"
        )

        average_cpu = utilization.get(
            "average_cpu"
        )

        samples = utilization.get(
            "samples",
            0
        )

        # ==================================================
        # NO RECOMMENDATION
        # ==================================================

        if recommendation in (
            "NO_ACTION",
            "NO_RECOMMENDATION"
        ):

            return {

                "agent":
                    self.name,

                "resource_id":
                    resource_id,

                "risk_level":
                    "LOW",

                "decision":
                    "DO_NOTHING",

                "reason":
                    "No optimization action "
                    "is currently required."
            }

        # ==================================================
        # NO CPU DATA
        # ==================================================

        if (
            cpu_status == "NO_DATA"
            or average_cpu is None
            or samples == 0
        ):

            return {

                "agent":
                    self.name,

                "resource_id":
                    resource_id,

                "risk_level":
                    "HIGH",

                "decision":
                    "DO_NOTHING",

                "reason":
                    "Insufficient CPU metrics "
                    "to safely evaluate the "
                    "optimization."
            }

        # ==================================================
        # STOPPED INSTANCE
        # ==================================================

        if resource_state == "stopped":

            return {

                "agent":
                    self.name,

                "resource_id":
                    resource_id,

                "risk_level":
                    "LOW",

                "decision":
                    "REVIEW",

                "reason":
                    "Instance is stopped. "
                    "Optimization should be "
                    "reviewed before making "
                    "changes."
            }

        # ==================================================
        # HIGH CPU
        # ==================================================

        if cpu_status == "HIGH_UTILIZATION":

            return {

                "agent":
                    self.name,

                "resource_id":
                    resource_id,

                "risk_level":
                    "HIGH",

                "decision":
                    "REVIEW",

                "reason":
                    "CPU utilization is high. "
                    "Automatic downsizing "
                    "could negatively affect "
                    "workload performance."
            }

        # ==================================================
        # UNDERUTILIZED
        # ==================================================

        if (
            cpu_status == "UNDERUTILIZED"
            and recommendation == "RIGHTSIZE_EC2"
        ):

            if samples >= 20:

                return {

                    "agent":
                        self.name,

                    "resource_id":
                        resource_id,

                    "risk_level":
                        "LOW",

                    "decision":
                        "REVIEW",

                    "reason":
                        "Resource is consistently "
                        "underutilized with "
                        "sufficient metric samples. "
                        "Rightsizing appears safe "
                        "but should be reviewed "
                        "before execution."
                }

            return {

                "agent":
                    self.name,

                "resource_id":
                    resource_id,

                "risk_level":
                    "MEDIUM",

                "decision":
                    "REVIEW",

                "reason":
                    "Resource appears "
                    "underutilized, but there "
                    "are not enough metric "
                    "samples for a high-confidence "
                    "optimization."
            }

        # ==================================================
        # LOW UTILIZATION
        # ==================================================

        if (
            cpu_status == "LOW_UTILIZATION"
            and recommendation == "REVIEW_EC2_USAGE"
        ):

            return {

                "agent":
                    self.name,

                "resource_id":
                    resource_id,

                "risk_level":
                    "MEDIUM",

                "decision":
                    "REVIEW",

                "reason":
                    "Resource has low CPU "
                    "utilization. Workload "
                    "requirements should be "
                    "reviewed before "
                    "rightsizing."
            }

        # ==================================================
        # DEFAULT
        # ==================================================

        return {

            "agent":
                self.name,

            "resource_id":
                resource_id,

            "risk_level":
                "MEDIUM",

            "decision":
                "REVIEW",

            "reason":
                "Optimization recommendation "
                "requires manual review."
        }
