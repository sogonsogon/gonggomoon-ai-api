from app.core.config import get_settings
from app.application.ports.ports import JobQueuePort
from app.infrastructure.queue.redis_queue import RedisJobQueue
from app.infrastructure.queue.cloud_tasks_queue import CloudTasksJobQueue
from app.infrastructure.db.session import create_session_factory
from app.infrastructure.db.extracted_experience_repository import SqlAlchemyExtractedExperienceRepository
from app.application.services.experiece_extraction_service import ExperienceExtractionService
from app.application.services.portfolio_strategy_generation_service import PortfolioStrategyGenerationService
from app.application.services.interview_strategy_generation_service import InterviewStrategyGenerationService
from app.application.services.post_analysis_service import PostAnalysisService

settings = get_settings()
session_factory = create_session_factory(settings.database_url)

##### Queue 구현체 선택 ######
def _create_queue(s=settings) -> JobQueuePort:
    if s.queue_provider == "cloud_tasks":
        return CloudTasksJobQueue(
            project=s.cloud_tasks_project,
            location=s.cloud_tasks_location,
            queue_name=s.cloud_tasks_queue_name,
            worker_url=s.cloud_tasks_worker_url,
            service_account_email=s.cloud_tasks_service_account_email,
            internal_api_key=s.internal_api_key,
        )
    # 기본값: Redis
    return RedisJobQueue(
        redis_url=s.redis_url,
        queue_key=s.redis_queue_key,
    )

queue: JobQueuePort = _create_queue()

##### API 서버 관련 의존성 주입 ######
extracted_experience_repository = SqlAlchemyExtractedExperienceRepository(session_factory=session_factory)

experience_extraction_service = ExperienceExtractionService(
    queue=queue,
    repository=extracted_experience_repository,
    callback_url=settings.call_back_url + "/experience-extraction"
)

portfolio_strategy_generation_service = PortfolioStrategyGenerationService(
    queue=queue,
    callback_url=settings.call_back_url + "/portfolio-strategy-generation"
)

interview_strategy_generation_service = InterviewStrategyGenerationService(
    queue=queue,
    callback_url=settings.call_back_url + "/interview-strategy-generation"
)

# NOTE : Post Analysis Service는 백오피스에서 사용할 예정이므로, 콜백 URL이 다릅니다.
post_analysis_service = PostAnalysisService(
    queue=queue,
    callback_url=settings.backoffice_callback_url + "/post-analysis"
)
