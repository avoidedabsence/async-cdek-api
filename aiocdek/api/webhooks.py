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
	async def subscribe_webhook(
		self, url: str, webhook_type: WebhookType = WebhookType.ORDER_STATUS
	) -> WebhookResponse:
		try:
			webhook_request = WebhookRequest(url=url, type=webhook_type)
			response = await self._post(
				"/v2/webhooks", json=webhook_request.model_dump(exclude_none=True)
			)
			return WebhookResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in subscribe_webhook: {e}")
			raise

	async def get_webhooks(self) -> list[WebhookInfo]:
		try:
			response = await self._get("/v2/webhooks")
			if isinstance(response, list):
				return [WebhookInfo(**webhook) for webhook in response]
			return [WebhookInfo(**response)]
		except ValidationError as e:
			logger.error(f"Validation error in get_webhooks: {e}")
			raise

	async def delete_webhook(self, uuid: str) -> dict[str, Any]:
		try:
			response = await self._delete(f"/v2/webhooks/{uuid}")
			return response
		except ValidationError as e:
			logger.error(f"Validation error in delete_webhook: {e}")
			raise
