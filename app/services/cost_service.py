from datetime import date, timedelta

from app.aws.cost_explorer import (
    get_cost_by_service
)

from app.database.models import Cost
from app.database.session import SessionLocal


def collect_and_save_costs(
    days=30
):
    """
    Collect AWS service-level costs from
    Cost Explorer and save them to PostgreSQL.
    """

    print("\n========================================")
    print("       AWS COST COLLECTION")
    print("========================================\n")

    end_date = date.today()

    start_date = (
        end_date
        - timedelta(days=days)
    )

    print(
        f"Collecting AWS costs from "
        f"{start_date} to {end_date}..."
    )

    # --------------------------------------------------
    # FETCH COSTS FROM AWS
    # --------------------------------------------------

    response = get_cost_by_service(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )

    results = response.get(
        "ResultsByTime",
        []
    )

    db = SessionLocal()

    saved_count = 0

    try:

        # --------------------------------------------------
        # PROCESS EACH DAY
        # --------------------------------------------------

        for result in results:

            period = result.get(
                "TimePeriod",
                {}
            )

            cost_date_string = period.get(
                "Start"
            )

            if not cost_date_string:
                continue

            cost_date = date.fromisoformat(
                cost_date_string
            )

            # --------------------------------------------------
            # PROCESS EACH AWS SERVICE
            # --------------------------------------------------

            for group in result.get(
                "Groups",
                []
            ):

                keys = group.get(
                    "Keys",
                    []
                )

                if not keys:
                    continue

                service = keys[0]

                amount = float(
                    group
                    .get("Metrics", {})
                    .get("UnblendedCost", {})
                    .get("Amount", 0)
                )

                # --------------------------------------------------
                # IGNORE ZERO-COST RECORDS
                # --------------------------------------------------

                if amount == 0:
                    continue

                # --------------------------------------------------
                # CHECK FOR EXISTING RECORD
                # --------------------------------------------------

                existing = (
                    db.query(Cost)
                    .filter(
                        Cost.service == service
                    )
                    .filter(
                        Cost.cost_date == cost_date
                    )
                    .first()
                )

                # --------------------------------------------------
                # UPDATE EXISTING RECORD
                # --------------------------------------------------

                if existing:

                    existing.amount = amount

                    print(
                        f"Updated: "
                        f"{cost_date} | "
                        f"{service} | "
                        f"${amount:.6f}"
                    )

                # --------------------------------------------------
                # CREATE NEW RECORD
                # --------------------------------------------------

                else:

                    cost = Cost(

                        resource_id=None,

                        service=service,

                        cost_date=cost_date,

                        amount=amount,

                        currency="USD"
                    )

                    db.add(cost)

                    saved_count += 1

                    print(
                        f"Saved: "
                        f"{cost_date} | "
                        f"{service} | "
                        f"${amount:.6f}"
                    )

        db.commit()

        print(
            f"\n✓ Cost collection completed."
        )

        print(
            f"✓ New cost records: "
            f"{saved_count}"
        )

    except Exception as error:

        db.rollback()

        print(
            "\n✗ Cost collection failed:"
        )

        print(error)

        raise

    finally:

        db.close()
