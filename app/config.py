import os

from dotenv import load_dotenv


load_dotenv()


AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-south-2"
)


DATABASE_HOST = os.getenv(
    "DATABASE_HOST",
    "localhost"
)

DATABASE_PORT = os.getenv(
    "DATABASE_PORT",
    "5432"
)

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "cloud_optimizer"
)

DATABASE_USER = os.getenv(
    "DATABASE_USER",
    "optimizer_user"
)

DATABASE_PASSWORD = os.getenv(
    "DATABASE_PASSWORD"

)

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:1.7b"
)
