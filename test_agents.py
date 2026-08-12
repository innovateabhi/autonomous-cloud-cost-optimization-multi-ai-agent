from app.agents.resource_agent import ResourceAgent
from app.agents.utilization_agent import UtilizationAgent
from app.agents.cost_agent import CostAgent
from app.agents.optimization_agent import OptimizationAgent
from app.agents.risk_agent import RiskAgent

print("\n--- RESOURCE AGENT ---")

resource_agent = ResourceAgent()

resource_context = {

    "resource_id":
        "i-demo123456",

    "resource_type":
        "EC2",

    "region":
        "ap-south-2",

    "state":
        "running",

    "instance_type":
        "t3.large"
}

resource_result = resource_agent.run(
    resource_context
)

print(resource_result)


print("\n--- UTILIZATION AGENT ---")

utilization_agent = UtilizationAgent()

utilization_context = {

    "resource_id":
        "i-demo123456",

    "cpu_values": [
        5.2,
        7.1,
        6.4,
        8.2,
        4.9
    ]
}

utilization_result = utilization_agent.run(
    utilization_context
)

print(utilization_result)


print("\n--- COST AGENT ---")

cost_agent = CostAgent()

cost_context = {

    "resource_id":
        "i-demo123456",

    "monthly_cost":
        82
}

cost_result = cost_agent.run(
    cost_context
)

print(cost_result)


print("\n--- OPTIMIZATION AGENT ---")

optimization_agent = OptimizationAgent()

optimization_context = {

    "resource":
        resource_result,

    "utilization":
        utilization_result,

    "cost":
        cost_result
}

optimization_result = optimization_agent.run(
    optimization_context
)

print(
    optimization_result
)

print("\n--- RISK AGENT ---")

risk_agent = RiskAgent()

risk_context = {

    "resource": {
        "resource_id": "i-demo123456",
        "resource_type": "EC2",
        "state": "running",
        "environment": "development"
    },

    "utilization": utilization_result,

    "optimization": optimization_result
}

risk_result = risk_agent.run(
    risk_context
)

print(risk_result)
