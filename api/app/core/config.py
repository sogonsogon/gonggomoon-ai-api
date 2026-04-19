from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    service_name: str = "ai-server"
    service_version: str = "0.1.0"
    internal_api_key: str = "local-dev-secret"
    worker_poll_interval_seconds: float = 1.0

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
    s3_bucket: str | None = None
    s3_region: str | None = None
    s3_prefix: str = ""
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    call_back_url: str | None = None
    backoffice_callback_url: str | None = None


def get_settings() -> Settings:
    poll_interval = float(getenv("WORKER_POLL_INTERVAL_SECONDS", "1.0"))
    return Settings(
        service_name=getenv("SERVICE_NAME", "ai-server"),
        service_version=getenv("SERVICE_VERSION", "0.1.0"),
        internal_api_key=getenv("INTERNAL_API_KEY", "local-dev-secret"),
        worker_poll_interval_seconds=poll_interval,
        queue_provider=getenv("QUEUE_PROVIDER", "redis"),
        redis_url=getenv("REDIS_URL", "redis://localhost:6379/0"),
        redis_queue_key=getenv("REDIS_QUEUE_KEY", "ai:jobs"),
        cloud_tasks_project=getenv("CLOUD_TASKS_PROJECT"),
        cloud_tasks_location=getenv("CLOUD_TASKS_LOCATION"),
        cloud_tasks_queue_name=getenv("CLOUD_TASKS_QUEUE_NAME"),
        cloud_tasks_worker_url=getenv("CLOUD_TASKS_WORKER_URL"),
        cloud_tasks_service_account_email=getenv("CLOUD_TASKS_SERVICE_ACCOUNT_EMAIL"),
        database_url=getenv("DATABASE_URL"),
        s3_bucket=getenv("S3_BUCKET"),
        s3_region=getenv("AWS_REGION"),
        s3_prefix=getenv("S3_PREFIX", ""),
        gemini_api_key=getenv("GEMINI_API_KEY"),
        gemini_model=getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        call_back_url=getenv("CALLBACK_URL", ""),
        backoffice_callback_url=getenv("BACKOFFICE_CALLBACK_URL", ""),
    )
