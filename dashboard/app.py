import os
import sys
from pathlib import Path

import psycopg
from flask import Flask, jsonify, render_template

# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DASHBOARD_DIR = BASE_DIR / "dashboard"

# ============================================================
# PYTHON IMPORT PATH FIX
# ============================================================

base_dir_string = str(BASE_DIR)

if base_dir_string in sys.path:
    sys.path.remove(base_dir_string)

sys.path.insert(0, base_dir_string)

dashboard_dir_string = str(DASHBOARD_DIR)

while dashboard_dir_string in sys.path:
    sys.path.remove(dashboard_dir_string)

# ============================================================
# LOAD .ENV
# ============================================================

ENV_FILE = BASE_DIR / ".env"


def load_env_file():

    if not ENV_FILE.exists():

        print(
            f"[WARNING] .env file not found: {ENV_FILE}"
        )

        return

    try:

        with ENV_FILE.open(
            "r",
            encoding="utf-8"
        ) as env_file:

            for raw_line in env_file:

                line = raw_line.strip()

                # Ignore empty lines
                if not line:
                    continue

                # Ignore comments
                if line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split(
                    "=",
                    1
                )

                key = key.strip()
                value = value.strip()

                # Remove surrounding quotes
                if (
                    len(value) >= 2
                    and value[0] == value[-1]
                    and value[0] in ("'", '"')
                ):
                    value = value[1:-1]

                # Do not overwrite an already-exported
                # environment variable.
                os.environ.setdefault(
                    key,
                    value
                )

        print(
            f"[OK] Loaded environment file: {ENV_FILE}"
        )

    except Exception as error:

        print(
            f"[WARNING] Could not load .env: {error}"
        )


load_env_file()

# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ============================================================
# DATABASE CONFIGURATION
# ============================================================


def get_database_config():

    """
    Return PostgreSQL configuration.

    Primary variables:

        DATABASE_HOST
        DATABASE_PORT
        DATABASE_NAME
        DATABASE_USER
        DATABASE_PASSWORD

    Older DB_* names are supported as fallback.
    """

    return {

        "host":
            os.getenv(
                "DATABASE_HOST",
                os.getenv(
                    "DB_HOST",
                    "localhost"
                )
            ),

        "port":
            os.getenv(
                "DATABASE_PORT",
                os.getenv(
                    "DB_PORT",
                    "5432"
                )
            ),

        "dbname":
            os.getenv(
                "DATABASE_NAME",
                os.getenv(
                    "DB_NAME",
                    "cloud_optimizer"
                )
            ),

        "user":
            os.getenv(
                "DATABASE_USER",
                os.getenv(
                    "DB_USER",
                    "optimizer_user"
                )
            ),

        "password":
            os.getenv(
                "DATABASE_PASSWORD",
                os.getenv(
                    "DB_PASSWORD"
                )
            )
    }


def get_db_connection():

    """
    Create a PostgreSQL connection.

    DATABASE_URL is supported if supplied.

    Otherwise DATABASE_* variables are used.
    """

    database_url = os.getenv(
        "DATABASE_URL"
    )

    if database_url:

        return psycopg.connect(
            database_url
        )

    config = get_database_config()

    return psycopg.connect(
        host=config["host"],
        port=config["port"],
        dbname=config["dbname"],
        user=config["user"],
        password=config["password"]
    )


# ============================================================
# DATABASE HELPER
# ============================================================


def fetch_all(
    query,
    params=None
):

    connection = get_db_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                params or ()
            )

            if cursor.description is None:
                return []

            columns = [
                column.name
                for column in cursor.description
            ]

            rows = cursor.fetchall()

            return [
                dict(
                    zip(
                        columns,
                        row
                    )
                )
                for row in rows
            ]

    finally:

        connection.close()


# ============================================================
# SERIALIZATION
# ============================================================


def serialize_value(value):

    if value is None:
        return None

    if hasattr(
        value,
        "isoformat"
    ):

        return value.isoformat()

    if hasattr(
        value,
        "__float__"
    ):

        try:

            return float(value)

        except Exception:

            pass

    return value


def serialize_rows(rows):

    result = []

    for row in rows:

        result.append({

            key:
                serialize_value(value)

            for key, value in row.items()

        })

    return result


# ============================================================
# AWS RESOURCE SYNCHRONIZATION
# ============================================================


def sync_aws_resources():

    """
    Synchronize AWS resources with PostgreSQL.

    Currently this synchronizes EC2 instances.

    AWS
        ↓
    EC2 collector
        ↓
    resource_service
        ↓
    PostgreSQL
    """

    print()
    print("-" * 60)
    print("       AWS RESOURCE SYNCHRONIZATION")
    print("-" * 60)

    try:

        from app.aws.ec2 import (
            collect_and_save_ec2_instances
        )

        print(
            "[AWS] Starting EC2 discovery..."
        )

        collect_and_save_ec2_instances()

        print(
            "[AWS] ✓ EC2 resources synchronized."
        )

        print("-" * 60)

        return {

            "success": True,

            "message":
                "AWS EC2 resources synchronized successfully."

        }

    except Exception as error:

        print(
            "[AWS] ✗ Resource synchronization failed."
        )

        print(
            f"{type(error).__name__}: {error}"
        )

        print("-" * 60)

        return {

            "success": False,

            "message":
                "AWS resource synchronization failed.",

            "error":
                str(error)

        }


# ============================================================
# FRONTEND
# ============================================================


@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# DASHBOARD
# ============================================================


@app.route("/api/dashboard")
def dashboard():

    try:

        # ----------------------------------------------------
        # RESOURCES
        # ----------------------------------------------------

        resources = fetch_all(
            """
            SELECT
                id,
                resource_id,
                resource_type,
                name,
                region,
                state,
                instance_type,
                environment
            FROM resources
            ORDER BY id
            """
        )

        resource_count = len(resources)

        running_count = sum(

            1

            for resource in resources

            if str(
                resource.get(
                    "state",
                    ""
                )
            ).lower() == "running"

        )

        stopped_count = sum(

            1

            for resource in resources

            if str(
                resource.get(
                    "state",
                    ""
                )
            ).lower() == "stopped"

        )

        # ----------------------------------------------------
        # LATEST METRICS
        # ----------------------------------------------------

        metrics = fetch_all(
            """
            SELECT DISTINCT ON (resource_id)
                resource_id,
                timestamp,
                cpu_average,
                cpu_maximum,
                cpu_minimum
            FROM metrics
            ORDER BY
                resource_id,
                timestamp DESC
            """
        )

        # ----------------------------------------------------
        # RESOURCE COSTS
        # ----------------------------------------------------

        resource_costs = fetch_all(
            """
            SELECT
                resource_id,
                COALESCE(
                    SUM(amount),
                    0
                ) AS total_cost
            FROM costs
            WHERE
                resource_id IS NOT NULL
                AND cost_date >=
                    CURRENT_DATE - INTERVAL '30 days'
            GROUP BY resource_id
            """
        )

        # ----------------------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------------------

        recommendations = fetch_all(
            """
            SELECT
                recommendation_type,
                risk_level,
                status,
                estimated_monthly_savings
            FROM recommendations
            ORDER BY created_at DESC
            """
        )

        # ----------------------------------------------------
        # AUDIT LOGS
        # ----------------------------------------------------

        audits = fetch_all(
            """
            SELECT
                id,
                resource_id,
                recommendation,
                priority,
                risk_level,
                decision,
                execution_action,
                execution_status,
                estimated_savings,
                llm_status,
                llm_model,
                llm_recommendation,
                created_at
            FROM audit_logs
            ORDER BY created_at DESC
            LIMIT 100
            """
        )

        # ----------------------------------------------------
        # POTENTIAL SAVINGS
        # ----------------------------------------------------

        potential_savings = sum(

            float(
                row["estimated_savings"]
            )

            for row in audits

            if row.get(
                "estimated_savings"
            ) is not None

        )

        # ----------------------------------------------------
        # REVIEW COUNT
        # ----------------------------------------------------

        review_count = sum(

            1

            for row in audits

            if str(
                row.get(
                    "decision",
                    ""
                )
            ).upper() == "REVIEW"

        )

        # ----------------------------------------------------
        # LLM SUCCESS RATE
        # ----------------------------------------------------

        llm_completed = sum(

            1

            for row in audits

            if str(
                row.get(
                    "llm_status",
                    ""
                )
            ).upper() == "COMPLETED"

        )

        llm_total = len(audits)

        llm_success_rate = (

            round(

                (
                    llm_completed
                    / llm_total
                ) * 100,

                1

            )

            if llm_total

            else 0

        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success":
                True,

            "status":
                "COMPLETED",

            "summary": {

                "resources":
                    resource_count,

                "running":
                    running_count,

                "stopped":
                    stopped_count,

                "review_required":
                    review_count,

                "potential_savings":
                    round(
                        potential_savings,
                        2
                    ),

                "llm_success_rate":
                    llm_success_rate

            },

            "resources":
                serialize_rows(
                    resources
                ),

            "metrics":
                serialize_rows(
                    metrics
                ),

            "resource_costs":
                serialize_rows(
                    resource_costs
                ),

            "recommendations":
                serialize_rows(
                    recommendations
                ),

            "audits":
                serialize_rows(
                    audits
                )

        })

    except Exception as error:

        print()
        print("=" * 60)
        print("DASHBOARD API ERROR")
        print("=" * 60)

        print(
            f"{type(error).__name__}: {error}"
        )

        print("=" * 60)

        return jsonify({

            "success":
                False,

            "status":
                "FAILED",

            "error":
                str(error),

            "message":
                "Could not load dashboard data."

        }), 500


# ============================================================
# RESOURCES
# ============================================================


@app.route("/api/resources")
def resources():

    try:

        rows = fetch_all(
            """
            SELECT
                id,
                resource_id,
                resource_type,
                name,
                region,
                state,
                instance_type,
                environment,
                discovered_at,
                updated_at
            FROM resources
            ORDER BY id
            """
        )

        return jsonify(
            serialize_rows(rows)
        )

    except Exception as error:

        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 500


# ============================================================
# RECOMMENDATIONS
# ============================================================


@app.route("/api/recommendations")
def recommendations():

    try:

        rows = fetch_all(
            """
            SELECT
                id,
                resource_id,
                recommendation_type,
                current_configuration,
                recommended_configuration,
                estimated_monthly_savings,
                currency,
                risk_level,
                reason,
                confidence,
                status,
                created_at
            FROM recommendations
            ORDER BY created_at DESC
            """
        )

        return jsonify(
            serialize_rows(rows)
        )

    except Exception as error:

        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 500


# ============================================================
# AUDIT LOGS
# ============================================================


@app.route("/api/audit-logs")
def audit_logs():

    try:

        rows = fetch_all(
            """
            SELECT
                id,
                resource_id,
                event_type,
                agent_name,
                recommendation,
                priority,
                risk_level,
                decision,
                execution_action,
                execution_status,
                estimated_savings,
                llm_status,
                llm_model,
                llm_recommendation,
                confidence,
                status,
                message,
                created_at
            FROM audit_logs
            ORDER BY created_at DESC
            LIMIT 200
            """
        )

        return jsonify(
            serialize_rows(rows)
        )

    except Exception as error:

        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 500


# ============================================================
# SINGLE RESOURCE
# ============================================================


@app.route(
    "/api/resource/<resource_id>"
)
def resource_details(
    resource_id
):

    try:

        rows = fetch_all(
            """
            SELECT
                id,
                resource_id,
                resource_type,
                name,
                region,
                state,
                instance_type,
                environment,
                tags,
                discovered_at,
                updated_at
            FROM resources
            WHERE resource_id = %s
            """,
            (
                resource_id,
            )
        )

        if not rows:

            return jsonify({

                "error":
                    "Resource not found"

            }), 404

        resource = rows[0]

        return jsonify(
            serialize_rows(
                [resource]
            )[0]
        )

    except Exception as error:

        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 500


# ============================================================
# SYNC AWS RESOURCES
# ============================================================


@app.route(
    "/api/sync-resources",
    methods=["POST"]
)
def sync_resources():

    """
    Manually synchronize AWS resources.

    Used by the dashboard Refresh button.

    Flow:

        Browser
            ↓
        POST /api/sync-resources
            ↓
        AWS EC2
            ↓
        PostgreSQL
    """

    result = sync_aws_resources()

    if result["success"]:

        return jsonify({

            "success":
                True,

            "status":
                "COMPLETED",

            "message":
                result["message"]

        })

    return jsonify({

        "success":
            False,

        "status":
            "FAILED",

        "message":
            result["message"],

        "error":
            result["error"]

    }), 500


# ============================================================
# RUN ANALYSIS
# ============================================================


@app.route(
    "/api/run-analysis",
    methods=["POST"]
)
def run_analysis():

    try:

        print()
        print("=" * 60)
        print(
            "       DASHBOARD ANALYSIS REQUEST"
        )
        print("=" * 60)

        # ----------------------------------------------------
        # VERIFY IMPORT PATH
        # ----------------------------------------------------

        print()

        print(
            f"Project root: {BASE_DIR}"
        )

        print(
            f"Python executable: {sys.executable}"
        )

        # ----------------------------------------------------
        # IMPORT ANALYSIS SERVICE
        # ----------------------------------------------------

        from app.services.analysis_service import (
            analyze_all_resources
        )

        from app.agents.llm_agent import (
            LLMAgent
        )

        print(
            "✓ Analysis modules imported successfully."
        )

        # ----------------------------------------------------
        # STEP 0 — AWS RESOURCE SYNCHRONIZATION
        # ----------------------------------------------------

        print()
        print(
            "[0/2] Synchronizing AWS EC2 resources..."
        )

        sync_result = sync_aws_resources()

        if not sync_result["success"]:

            return jsonify({

                "success":
                    False,

                "status":
                    "FAILED",

                "message":
                    "AWS resource synchronization failed.",

                "error":
                    sync_result["error"]

            }), 500

        print(
            "✓ AWS resources synchronized."
        )

        # ----------------------------------------------------
        # STEP 1 — DECISION ENGINE
        # ----------------------------------------------------

        print()
        print(
            "[1/2] Running cloud resource analysis..."
        )

        results = analyze_all_resources(
            hours=24
        )

        if not results:

            return jsonify({

                "success":
                    True,

                "status":
                    "COMPLETED",

                "message":
                    (
                        "Analysis completed, "
                        "but no resources were found."
                    ),

                "resources_analyzed":
                    0,

                "results":
                    []

            })

        print(
            f"✓ Resources analyzed: "
            f"{len(results)}"
        )

        # ----------------------------------------------------
        # STEP 2 — OLLAMA
        # ----------------------------------------------------

        print()
        print(
            "[2/2] Running Ollama AI analysis..."
        )

        llm_agent = LLMAgent()

        print(
            f"✓ Ollama model: "
            f"{llm_agent.model}"
        )

        print(
            f"✓ Ollama host: "
            f"{llm_agent.ollama_host}"
        )

        llm_results = []

        # ----------------------------------------------------
        # PROCESS EVERY RESOURCE
        # ----------------------------------------------------

        for result in results:

            resource = result.get(
                "resource",
                {}
            )

            resource_id = resource.get(
                "resource_id",
                "UNKNOWN"
            )

            print()
            print(
                f"Generating AI recommendation "
                f"for {resource_id}..."
            )

            context = {

                "resource":
                    result.get(
                        "resource",
                        {}
                    ),

                "utilization":
                    result.get(
                        "utilization",
                        {}
                    ),

                "cost":
                    result.get(
                        "cost",
                        {}
                    ),

                "optimization":
                    result.get(
                        "optimization",
                        {}
                    ),

                "risk":
                    result.get(
                        "risk",
                        {}
                    )

            }

            try:

                llm_result = llm_agent.run(
                    context
                )

                result["llm"] = (
                    llm_result
                )

                llm_results.append({

                    "resource_id":
                        resource_id,

                    "status":
                        llm_result.get(
                            "status",
                            "UNKNOWN"
                        )

                })

                print(
                    f"✓ AI recommendation generated "
                    f"for {resource_id}"
                )

            except Exception as error:

                print(
                    f"✗ LLM failed for "
                    f"{resource_id}"
                )

                print(
                    f"Error: {error}"
                )

                result["llm"] = {

                    "agent":
                        "LLM Recommendation Agent",

                    "status":
                        "FAILED",

                    "error":
                        str(error)

                }

                llm_results.append({

                    "resource_id":
                        resource_id,

                    "status":
                        "FAILED",

                    "error":
                        str(error)

                })

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        successful_llm = sum(

            1

            for item in llm_results

            if item.get(
                "status"
            ) == "COMPLETED"

        )

        print()
        print("=" * 60)
        print(
            "       ANALYSIS COMPLETED"
        )
        print("=" * 60)

        return jsonify({

            "success":
                True,

            "status":
                "COMPLETED",

            "message":
                "Cloud analysis completed successfully.",

            "resources_analyzed":
                len(results),

            "llm_successful":
                successful_llm,

            "llm_total":
                len(llm_results),

            "results":
                results

        })

    except Exception as error:

        print()
        print("=" * 60)
        print(
            "       ANALYSIS FAILED"
        )
        print("=" * 60)

        print(
            f"{type(error).__name__}: {error}"
        )

        print("=" * 60)

        return jsonify({

            "success":
                False,

            "status":
                "FAILED",

            "message":
                "Cloud analysis failed.",

            "error":
                str(error)

        }), 500


# ============================================================
# COMPATIBILITY ROUTE
# ============================================================


@app.route(
    "/api/analyze",
    methods=["POST"]
)
def analyze_compatibility():

    return run_analysis()


# ============================================================
# HEALTH
# ============================================================


@app.route("/api/health")
def health():

    database = False
    database_error = None

    ollama = False
    ollama_error = None

    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    try:

        connection = get_db_connection()

        connection.close()

        database = True

    except Exception as error:

        database_error = (
            f"{type(error).__name__}: {error}"
        )

        print(
            f"[HEALTH] Database error: "
            f"{database_error}"
        )

    # --------------------------------------------------------
    # OLLAMA
    # --------------------------------------------------------

    try:

        import requests

        ollama_host = os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434"
        ).rstrip("/")

        response = requests.get(
            f"{ollama_host}/api/tags",
            timeout=5
        )

        ollama = (
            response.status_code == 200
        )

        if not ollama:

            ollama_error = (
                f"Ollama returned HTTP "
                f"{response.status_code}"
            )

    except Exception as error:

        ollama_error = (
            f"{type(error).__name__}: {error}"
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return jsonify({

        "status":
            "healthy"
            if database and ollama
            else "degraded",

        "database":
            database,

        "database_error":
            database_error,

        "ollama":
            ollama,

        "ollama_error":
            ollama_error

    })


# ============================================================
# CONFIGURATION / DEBUG INFO
# ============================================================


@app.route("/api/config")
def config():

    """
    Safe configuration endpoint.

    PostgreSQL password is NEVER returned.
    """

    database = get_database_config()

    return jsonify({

        "project_root":
            str(BASE_DIR),

        "python":
            sys.executable,

        "database": {

            "host":
                database["host"],

            "port":
                database["port"],

            "name":
                database["dbname"],

            "user":
                database["user"],

            "password_configured":
                bool(
                    database["password"]
                )

        },

        "ollama": {

            "host":
                os.getenv(
                    "OLLAMA_HOST",
                    "http://localhost:11434"
                ),

            "model":
                os.getenv(
                    "OLLAMA_MODEL",
                    "qwen3:1.7b"
                )

        }

    })


# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":

    print()
    print("=" * 60)

    print(
        " AUTONOMOUS CLOUD COST OPTIMIZATION DASHBOARD"
    )

    print("=" * 60)
    print()

    print(
        f"Project root: {BASE_DIR}"
    )

    print(
        f"Python: {sys.executable}"
    )

    print()

    database_config = (
        get_database_config()
    )

    print(
        "PostgreSQL:"
    )

    print(
        f"  Host: "
        f"{database_config['host']}"
    )

    print(
        f"  Port: "
        f"{database_config['port']}"
    )

    print(
        f"  Database: "
        f"{database_config['dbname']}"
    )

    print(
        f"  User: "
        f"{database_config['user']}"
    )

    print(
        f"  Password configured: "
        f"{bool(database_config['password'])}"
    )

    print()

    print(
        "AWS:"
    )

    print(
        f"  Region: "
        f"{os.getenv(
            'AWS_REGION',
            'not configured'
        )}"
    )

    print()

    print(
        "Ollama:"
    )

    print(
        f"  Host: "
        f"{os.getenv(
            'OLLAMA_HOST',
            'http://localhost:11434'
        )}"
    )

    print(
        f"  Model: "
        f"{os.getenv(
            'OLLAMA_MODEL',
            'qwen3:1.7b'
        )}"
    )

    print()

    print(
        "Dashboard:"
    )

    print(
        "  http://localhost:5000"
    )

    print()

    print(
        "API:"
    )

    print(
        "  http://localhost:5000/api/dashboard"
    )

    print(
        "  http://localhost:5000/api/health"
    )

    print(
        "  http://localhost:5000/api/sync-resources"
    )

    print(
        "  http://localhost:5000/api/run-analysis"
    )

    print()

    print("=" * 60)
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
