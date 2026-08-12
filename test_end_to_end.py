import os
import subprocess
import sys

import requests
import psycopg

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# HEADER
# ============================================================

print()
print("=" * 60)
print("       END-TO-END PROJECT VALIDATION")
print("=" * 60)
print()


results = []


# ============================================================
# HELPER FUNCTION
# ============================================================

def run_test(name, command, timeout=300):

    print("-" * 60)
    print(f"[TEST] {name}")
    print("-" * 60)

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:

            print(f"✓ {name}: PASSED")

            if result.stdout.strip():
                print(result.stdout)

            return True

        print(f"✗ {name}: FAILED")

        if result.stdout.strip():
            print()
            print("STDOUT:")
            print(result.stdout)

        if result.stderr.strip():
            print()
            print("STDERR:")
            print(result.stderr)

        return False

    except subprocess.TimeoutExpired:

        print(
            f"✗ {name}: TIMEOUT "
            f"(>{timeout} seconds)"
        )

        return False

    except Exception as error:

        print(
            f"✗ {name}: {error}"
        )

        return False


# ============================================================
# 1. PYTHON ENVIRONMENT
# ============================================================

print("[1/6] Python environment")

print(
    f"Python: "
    f"{sys.version.split()[0]}"
)

print(
    f"Executable: "
    f"{sys.executable}"
)

print("✓ Python environment: PASSED")

results.append(True)

print()


# ============================================================
# 2. POSTGRESQL CONNECTIVITY
# ============================================================

print("[2/6] PostgreSQL connectivity")

try:

    database_url = os.getenv(
        "DATABASE_URL"
    )

    if database_url:

        connection = psycopg.connect(
            database_url
        )

    else:

        connection = psycopg.connect(

            host=os.getenv(
                "DATABASE_HOST",
                "localhost"
            ),

            port=os.getenv(
                "DATABASE_PORT",
                "5432"
            ),

            dbname=os.getenv(
                "DATABASE_NAME",
                "cloud_optimizer"
            ),

            user=os.getenv(
                "DATABASE_USER",
                "optimizer_user"
            ),

            password=os.getenv(
                "DATABASE_PASSWORD"
            )
        )

    cursor = connection.cursor()


    # --------------------------------------------------------
    # Resources
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM resources"
    )

    resource_count = (
        cursor.fetchone()[0]
    )


    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM metrics"
    )

    metric_count = (
        cursor.fetchone()[0]
    )


    # --------------------------------------------------------
    # Costs
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM costs"
    )

    cost_count = (
        cursor.fetchone()[0]
    )


    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM recommendations"
    )

    recommendation_count = (
        cursor.fetchone()[0]
    )


    # --------------------------------------------------------
    # Audit Logs
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM audit_logs"
    )

    audit_count = (
        cursor.fetchone()[0]
    )


    cursor.close()
    connection.close()


    print(
        f"Resources in database: "
        f"{resource_count}"
    )

    print(
        f"Metrics in database: "
        f"{metric_count}"
    )

    print(
        f"Costs in database: "
        f"{cost_count}"
    )

    print(
        f"Recommendations in database: "
        f"{recommendation_count}"
    )

    print(
        f"Audit logs in database: "
        f"{audit_count}"
    )

    print(
        "✓ PostgreSQL: PASSED"
    )

    results.append(True)


except Exception as error:

    print(
        "✗ PostgreSQL: FAILED"
    )

    print(error)

    results.append(False)


print()


# ============================================================
# 3. ANALYSIS SERVICE
# ============================================================

results.append(
    run_test(
        "Analysis Service",
        [
            sys.executable,
            "test_analysis_service.py"
        ],
        timeout=180
    )
)

print()


# ----------------------------------------------------------
# 4. Ollama LLM availability
# ----------------------------------------------------------

print("[4/6] Ollama LLM availability")

try:

    response = requests.get(
        "http://localhost:11434/api/tags",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    models = [
        model.get("name")
        for model in data.get("models", [])
    ]

    if "qwen3:1.7b" in models:

        print("✓ Ollama LLM: PASSED")
        print("Model available: qwen3:1.7b")

        results.append(True)

    else:

        print("✗ Ollama LLM: FAILED")
        print("qwen3:1.7b model not found")

        results.append(False)

except Exception as error:

    print("✗ Ollama LLM: FAILED")
    print(error)

    results.append(False)

print()

# ============================================================
# 5. AUDIT LOGGING
# ============================================================

results.append(
    run_test(
        "Audit Logging",
        [
            sys.executable,
            "test_audit_logging.py"
        ],
        timeout=180
    )
)

print()


# ============================================================
# 6. OLLAMA HEALTH CHECK
# ============================================================

print("[6/6] Ollama connectivity")

try:

    ollama_host = os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434"
    )

    ollama_model = os.getenv(
        "OLLAMA_MODEL",
        "qwen3:1.7b"
    )


    # --------------------------------------------------------
    # Remove accidental trailing slash
    # --------------------------------------------------------

    ollama_host = ollama_host.rstrip("/")


    # --------------------------------------------------------
    # Check Ollama
    # --------------------------------------------------------

    response = requests.get(
        f"{ollama_host}/api/tags",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()


    models = [

        model.get("name")

        for model in
        data.get("models", [])

    ]


    print(
        "Ollama host:",
        ollama_host
    )

    print(
        "Available Ollama models:",
        ", ".join(models)
        if models
        else "None"
    )


    if ollama_model in models:

        print(
            f"✓ Ollama model found: "
            f"{ollama_model}"
        )

        print(
            "✓ Ollama: PASSED"
        )

        results.append(True)

    else:

        print(
            f"✗ Required model "
            f"'{ollama_model}' "
            f"was not found."
        )

        results.append(False)


except Exception as error:

    print(
        "✗ Ollama: FAILED"
    )

    print(error)

    results.append(False)


# ============================================================
# VALIDATION SUMMARY
# ============================================================

print()
print("=" * 60)
print("                 VALIDATION SUMMARY")
print("=" * 60)

passed = sum(results)
total = len(results)

print(
    f"Tests passed : "
    f"{passed}/{total}"
)


if passed == total:

    print()
    print(
        "✓ END-TO-END VALIDATION PASSED"
    )

    print()

    print(
        "System flow validated:"
    )

    print(
        "AWS Resources"
        " → Metrics"
        " → Analysis"
        " → Optimization"
        " → Risk"
        " → Decision"
    )

    print(
        "Decision"
        " → Ollama LLM"
        " → Audit Logging"
        " → PostgreSQL"
    )

    print()

    sys.exit(0)


else:

    print()

    print(
        "⚠ SOME VALIDATION TESTS FAILED"
    )

    print(
        "Fix the failed component "
        "before final presentation."
    )

    print()

    sys.exit(1)
