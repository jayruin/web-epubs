from typing import Any, Optional

from more_itertools import consume

from .app_worker import AppWorker
from .build_jobs import (
    BaseBuildJob,
    EPUB2BuildJob,
    EPUB3BuildJob,
    EPUBType,
    PaginatedImagesBuildJob
)
from app.settings import Settings
from core.runner import pool_run


class Builder(AppWorker):
    def build_projects(
        self,
        projects: list[str],
        project_type: str,
        bundles: list[str]
    ) -> None:
        args_collection: list[tuple[Settings, str, EPUBType, list[str]]] = []
        kwargs_collection: list[dict[str, Any]] = []
        for project in projects:
            args_collection.append(
                (self.settings, project, EPUBType(project_type), bundles)
            )
            kwargs_collection.append({})
        consume(
            pool_run(
                build_epub,
                args_collection,
                kwargs_collection,
                "process",
                show_progress=True
            )
        )


def build_epub(
    settings: Settings,
    project: str,
    epub_type: EPUBType,
    bundles: list[str]
) -> None:
    build_job_types: list[type[BaseBuildJob]] = [
        EPUB2BuildJob,
        EPUB3BuildJob,
        PaginatedImagesBuildJob
    ]
    build_job: Optional[BaseBuildJob] = None
    for build_job_type in build_job_types:
        if build_job_type.epub_type is epub_type:
            build_job = build_job_type(settings, project, bundles)
    assert build_job is not None
    build_job.run()
