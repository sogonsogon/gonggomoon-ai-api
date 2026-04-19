from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    service_name: str = "ai-server"
    service_version: str = "0.1.0"
    internal_api_key: str = "local-dev-secret"

    # Queue provider: "redis" | "cloud_tasks"
    queue_provider: str = "redis"

    # Redis 설정 (queue_provider="redis" 일 때 사용)
    redis_url: str = "redis://localhost:6379/0"
    redis_queue_key: str = "ai:jobs"

    # Cloud Tasks 설정 (queue_provider="cloud_tasks" 일 때 사용)
    cloud_tasks_project: str | None = None
    cloud_tasks_location: str | None = None
    cloud_tasks_queue_name: str | None = None
    cloud_tasks_worker_url: str | None = None
    cloud_tasks_service_account_email: str | None = None

    database_url: str | None = None
    call_back_url: str = ""
    backoffice_callback_url: str = ""


def get_settings() -> Settings:
    return Settings(
        service_name=getenv("SERVICE_NAME", "ai-server"),
        service_version=getenv("SERVICE_VERSION", "0.1.0"),
        internal_api_key=getenv("INTERNAL_API_KEY", "local-dev-secret"),
        queue_provider=getenv("QUEUE_PROVIDER", "redis"),
        redis_url=getenv("REDIS_URL", "redis://localhost:6379/0"),
        redis_queue_key=getenv("REDIS_QUEUE_KEY", "ai:jobs"),
        cloud_tasks_project=getenv("CLOUD_TASKS_PROJECT"),
        cloud_tasks_location=getenv("CLOUD_TASKS_LOCATION"),
        cloud_tasks_queue_name=getenv("CLOUD_TASKS_QUEUE_NAME"),
        cloud_tasks_worker_url=getenv("CLOUD_TASKS_WORKER_URL"),
        cloud_tasks_service_account_email=getenv("CLOUD_TASKS_SERVICE_ACCOUNT_EMAIL"),
        database_url=getenv("DATABASE_URL"),
        call_back_url=getenv("CALLBACK_URL", ""),
        backoffice_callback_url=getenv("BACKOFFICE_CALLBACK_URL", ""),
    )
