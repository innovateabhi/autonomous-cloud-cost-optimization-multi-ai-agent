from app.agents.resource_agent import ResourceAgent
from app.agents.utilization_agent import UtilizationAgent
from app.agents.cost_agent import CostAgent
from app.agents.optimization_agent import OptimizationAgent
from app.agents.risk_agent import RiskAgent
from app.agents.llm_agent import LLMAgent


class AgentOrchestrator:

    def __init__(self):

        self.resource_agent = ResourceAgent()

        self.utilization_agent = UtilizationAgent()

        self.cost_agent = CostAgent()

        self.optimization_agent = OptimizationAgent()

        self.risk_agent = RiskAgent()

        self.llm_agent = LLMAgent()

    def run(self, resource):

        print("\n========================================")
        print("       AUTONOMOUS CLOUD OPTIMIZER")
        print("========================================\n")

        # --------------------------------------------------
        # 1. RESOURCE AGENT
        # --------------------------------------------------

        print("[1] Running Resource Agent...")

        resource_result = self.resource_agent.run(
            resource
        )

        print("✓ Resource Agent completed.")

        # --------------------------------------------------
        # 2. UTILIZATION AGENT
        # --------------------------------------------------

        print("\n[2] Running Utilization Agent...")

        utilization_result = (
            self.utilization_agent.run(
                resource
            )
        )

        print("✓ Utilization Agent completed.")

        # --------------------------------------------------
        # 3. COST AGENT
        # --------------------------------------------------

        print("\n[3] Running Cost Agent...")

        cost_result = self.cost_agent.run(
            resource
        )

        print("✓ Cost Agent completed.")

        # --------------------------------------------------
        # 4. OPTIMIZATION AGENT
        # --------------------------------------------------

        print("\n[4] Running Optimization Agent...")

        optimization_context = {

            "resource":
                resource_result,

            "utilization":
                utilization_result,

            "cost":
                cost_result
        }

        optimization_result = (
            self.optimization_agent.run(
                optimization_context
            )
        )

        print("✓ Optimization Agent completed.")

        # --------------------------------------------------
        # 5. RISK AGENT
        # --------------------------------------------------

        print("\n[5] Running Risk Agent...")

        risk_context = {

            "resource":
                resource_result,

            "utilization":
                utilization_result,

            "cost":
                cost_result,

            "optimization":
                optimization_result
        }

        risk_result = (
            self.risk_agent.run(
                risk_context
            )
        )

        print("✓ Risk Agent completed.")

        # --------------------------------------------------
        # 6. LLM AGENT
        # --------------------------------------------------

        print("\n[6] Running LLM Agent...")

        llm_context = {

            "resource":
                resource_result,

            "utilization":
                utilization_result,

            "cost":
                cost_result,

            "optimization":
                optimization_result,

            "risk":
                risk_result
        }

        llm_result = (
            self.llm_agent.run(
                llm_context
            )
        )

        print("✓ LLM Agent completed.")

        # --------------------------------------------------
        # FINAL RESULT
        # --------------------------------------------------

        final_result = {

            "resource":
                resource_result,

            "utilization":
                utilization_result,

            "cost":
                cost_result,

            "optimization":
                optimization_result,

            "risk":
                risk_result,

            "llm":
                llm_result
        }

        print(
            "\n========================================"
        )

        print(
            "       PIPELINE COMPLETED"
        )

        print(
            "========================================\n"
        )

        return final_result
