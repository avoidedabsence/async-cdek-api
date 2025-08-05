from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import AsyncGenerator

from loguru import logger
from aiohttp import ClientSession
from pydantic import BaseModel

from .common import APIClient
from ..api import (
	CalculatorMixin,
	OrdersMixin,
	LocationsMixin,
	DeliveryPointsMixin,
	CourierMixin,
	PrintingMixin,
	WebhooksMixin,
)


class CDEKAuthData(BaseModel):
	access_token: str
	expires_at: datetime

	def is_expired(self):
		return datetime.now() > self.expires_at


class CDEKAPIClient(
	APIClient,
	CalculatorMixin,
	OrdersMixin,
	LocationsMixin,
	DeliveryPointsMixin,
	CourierMixin,
	PrintingMixin,
	WebhooksMixin,
):
	_cached_auth_data: CDEKAuthData = None
	_client_name = __qualname__
	_client_id: str = None
	_client_secret: str = None

	@classmethod
	def __init__(cls, client_id: str, client_secret: str, test_environment: bool = False, debug: bool = False):
		cls._client_id = client_id
		cls._client_secret = client_secret
		cls._base_url = "https://api.cdek.ru/" if not test_environment else "https://api.edu.cdek.ru/"
		cls._debug_mode = debug

	@classmethod
	@asynccontextmanager
	async def _get_cached_auth_data(cls) -> AsyncGenerator[CDEKAuthData | None]:
		if cls._cached_auth_data and not cls._cached_auth_data.is_expired():
			logger.debug("Retrieved cached AuthData")
			yield cls._cached_auth_data
			return

		logger.debug("Requesting new AuthData")
		async with ClientSession() as session:
			auth_request = await session.post(
				"https://api.cdek.ru/v2/oauth/token",
				data={
					"grant_type": "client_credentials",
					"client_id": cls._client_id,
					"client_secret": cls._client_secret,
				},
			)
			if auth_request.ok:
				data = await auth_request.json()
				access_token = data["access_token"]
				expires_at = datetime.now() + timedelta(seconds=data["expires_in"])
				cls._cached_auth_data = CDEKAuthData(
					access_token=access_token, expires_at=expires_at
				)
				yield cls._cached_auth_data
			else:
				logger.error(await auth_request.text())
				yield None
