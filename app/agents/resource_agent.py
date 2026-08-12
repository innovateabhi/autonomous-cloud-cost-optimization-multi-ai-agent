from app.agents.base_agent import BaseAgent


class ResourceAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Resource Agent"
        )

    def run(self, context):

        resource_id = context.get(
            "resource_id"
        )

        resource_type = context.get(
            "resource_type"
        )

        region = context.get(
            "region"
        )

        state = context.get(
            "state"
        )

        return {
            "agent": self.name,
            "resource_id": resource_id,
            "resource_type": resource_type,
            "region": region,
            "state": state
        }
