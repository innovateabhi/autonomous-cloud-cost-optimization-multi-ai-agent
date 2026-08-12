from datetime import datetime, timedelta

from app.aws.cost_explorer import (
    get_cost_by_service,
    summarize_service_costs
)


end_date = datetime.utcnow().date()

start_date = end_date - timedelta(days=7)


response = get_cost_by_service(
    start_date=start_date.isoformat(),
    end_date=end_date.isoformat()
)


summary = summarize_service_costs(response)


print("=" * 60)
print("AWS COST SUMMARY")
print("=" * 60)

print(f"Total Cost: {summary['total_cost']:.4f} USD")

print("\nCost By Service:")
print("-" * 60)


for service, cost in summary["service_costs"].items():

    print(
        f"{service}: "
        f"{cost:.4f} USD"
    )
