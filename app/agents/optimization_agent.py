from app.agents.base_agent import BaseAgent


class OptimizationAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Optimization Agent"
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

        cost = context.get(
            "cost",
            {}
        )

        resource_id = resource.get(
            "resource_id"
        )

        resource_type = resource.get(
            "resource_type"
        )

        instance_type = resource.get(
            "instance_type"
        )

        utilization_status = utilization.get(
            "status"
        )

        average_cpu = utilization.get(
            "average_cpu"
        )

        monthly_cost = cost.get(
            "monthly_cost"
        )

        cost_level = cost.get(
            "cost_level"
        )

        # ------------------------------------------------
        # EC2 RIGHT-SIZING
        # ------------------------------------------------

        if (
            resource_type == "EC2"
            and utilization_status == "UNDERUTILIZED"
            and monthly_cost is not None
        ):

            return {

                "agent": self.name,

                "resource_id": resource_id,

                "recommendation": "RIGHTSIZE_EC2",

                "priority": "HIGH",

                "reason": (
                    f"EC2 instance {resource_id} "
                    f"has an average CPU utilization "
                    f"of {average_cpu}% and costs "
                    f"approximately ${monthly_cost} "
                    f"per month."
                ),

                "current_instance_type":
                    instance_type,

                "cost_level":
                    cost_level,

                "estimated_savings":
                    round(
                        monthly_cost * 0.30,
                        2
                    )
            }

        # ------------------------------------------------
        # LOW UTILIZATION
        # ------------------------------------------------

        if (
            resource_type == "EC2"
            and utilization_status == "LOW_UTILIZATION"
        ):

            return {

                "agent": self.name,

                "resource_id": resource_id,

                "recommendation":
                    "REVIEW_EC2_USAGE",

                "priority":
                    "MEDIUM",

                "reason": (
                    "EC2 instance shows "
                    "low utilization. "
                    "Review workload requirements "
                    "before rightsizing."
                ),

                "current_instance_type":
                    instance_type,

                "estimated_savings":
                    0
            }

        # ------------------------------------------------
        # NORMAL UTILIZATION
        # ------------------------------------------------

        if (
            resource_type == "EC2"
            and utilization_status == "NORMAL"
        ):

            return {

                "agent": self.name,

                "resource_id": resource_id,

                "recommendation":
                    "NO_ACTION",

                "priority":
                    "LOW",

                "reason":
                    "Resource utilization "
                    "appears normal.",

                "current_instance_type":
                    instance_type,

                "estimated_savings":
                    0
            }

        # ------------------------------------------------
        # HIGH UTILIZATION
        # ------------------------------------------------

        if (
            resource_type == "EC2"
            and utilization_status == "HIGH_UTILIZATION"
        ):

            return {

                "agent": self.name,

                "resource_id": resource_id,

                "recommendation":
                    "CONSIDER_SCALING",

                "priority":
                    "MEDIUM",

                "reason": (
                    "EC2 instance has high "
                    "CPU utilization. "
                    "Downsizing is not recommended."
                ),

                "current_instance_type":
                    instance_type,

                "estimated_savings":
                    0
            }

        # ------------------------------------------------
        # UNKNOWN / UNSUPPORTED RESOURCE
        # ------------------------------------------------

        return {

            "agent": self.name,

            "resource_id":
                resource_id,

            "recommendation":
                "NO_RECOMMENDATION",

            "priority":
                "LOW",

            "reason":
                "Insufficient data or "
                "unsupported resource type.",

            "estimated_savings":
                0
        }
