from fastapi import APIRouter
from typing import Any, Callable
from app.core.responses import DEFAULT_ERROR_RESPONSES


class APIRouterWithErrors(APIRouter):

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        responses: dict[int | str, dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> None:

        merged_responses: dict[int | str, dict[str, Any]] = {
            **DEFAULT_ERROR_RESPONSES
        }

        if responses:
            merged_responses.update(responses)

        super().add_api_route(
            path=path,
            endpoint=endpoint,
            responses=merged_responses,
            **kwargs,
        )