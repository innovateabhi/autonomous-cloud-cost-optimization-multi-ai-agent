from sqlalchemy import text

from app.database.connection import engine


try:

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT current_database();")
        )

        database_name = result.scalar()

        print(
            f"Connected successfully to: "
            f"{database_name}"
        )


except Exception as error:

    print("Database connection failed.")

    print(error)
