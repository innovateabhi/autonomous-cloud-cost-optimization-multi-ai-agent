from datetime import datetime, timedelta

from app.aws.cost_explorer import get_cost_and_usage


end_date = datetime.utcnow().date()

start_date = end_date - timedelta(days=7)


response = get_cost_and_usage(
    start_date=start_date.isoformat(),
    end_date=end_date.isoformat()
)


for result in response["ResultsByTime"]:

    period = result["TimePeriod"]

    amount = result["Total"]["UnblendedCost"]["Amount"]

    unit = result["Total"]["UnblendedCost"]["Unit"]

    print(
        f"{period['Start']} → "
        f"{period['End']} : "
        f"{amount} {unit}"
    )
