from app.services.cost_service import (
    collect_and_save_costs
)


print("\n========================================")
print("       COST SERVICE TEST")
print("========================================\n")


collect_and_save_costs(
    days=30
)


print("\n========================================")
print("       TEST COMPLETED")
print("========================================\n")
