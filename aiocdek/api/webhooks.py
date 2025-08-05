from typing import Any
from pydantic import ValidationError
from loguru import logger

from ..models import (
	WebhookRequest,
	WebhookResponse,
	WebhookInfo,
)

from ..enums import WebhookType


class WebhooksMixin:
	@classmethod
	async def subscribe_webhook(
		cls, url: str, webhook_type: WebhookType = WebhookType.ORDER_STATUS
	) -> WebhookResponse:
		try:
			webhook_request = WebhookRequest(url=url, type=webhook_type)
			response = await cls._post(
				"/v2/webhooks", json=webhook_request.model_dump(exclude_none=True)
			)
			return WebhookResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in subscribe_webhook: {e}")
			raise

	@classmethod
	async def get_webhooks(cls) -> list[WebhookInfo]:
		try:
			response = await cls._get("/v2/webhooks")
			if isinstance(response, list):
				return [WebhookInfo(**webhook) for webhook in response]
			return [WebhookInfo(**response)]
		except ValidationError as e:
			logger.error(f"Validation error in get_webhooks: {e}")
			raise

	@classmethod
	async def delete_webhook(cls, uuid: str) -> dict[str, Any]:
		try:
			response = await cls._delete(f"/v2/webhooks/{uuid}")
			return response
		except ValidationError as e:
			logger.error(f"Validation error in delete_webhook: {e}")
			raise
