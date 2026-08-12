from app.services.cost_attribution_service import (
    get_cost_attribution
)


resource_id = "i-0e6178ff13b9b326b"


print("\n========================================")
print("       COST ATTRIBUTION TEST")
print("========================================")


result = get_cost_attribution(
    resource_id=resource_id,
    days=30
)


print(
    f"\nMonthly Cost: "
    f"${result['monthly_cost']}"
)

print(
    f"Cost Source: "
    f"{result['cost_source']}"
)

print(
    f"Confidence: "
    f"{result['confidence']}"
)

if "note" in result:

    print(
        f"Note: "
        f"{result['note']}"
    )


print("\n========================================")
print("       TEST COMPLETED")
print("========================================")
