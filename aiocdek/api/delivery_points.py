from pydantic import ValidationError
from loguru import logger
from ..models import (
	DeliveryPointFilter,
	DeliveryPoint,
	DeliveryPointSearchResult,
)


class DeliveryPointsMixin:
	@classmethod
	async def get_delivery_points(
		cls, filter_params: DeliveryPointFilter | None = None
	) -> list[DeliveryPoint]:
		try:
			params = (
				filter_params.model_dump(exclude_none=True) if filter_params else {}
			)
			response = await cls._get("/v2/deliverypoints", params=params)
			if isinstance(response, list):
				return [DeliveryPoint(**point) for point in response]
			return [DeliveryPoint(**response)]
		except ValidationError as e:
			logger.error(f"Validation error in get_delivery_points: {e}")
			raise

	@classmethod
	async def search_delivery_points(
		cls, filter_params: DeliveryPointFilter | None = None
	) -> DeliveryPointSearchResult:
		try:
			params = (
				filter_params.model_dump(exclude_none=True) if filter_params else {}
			)
			response = await cls._get("/v2/deliverypoints", params=params)
			return DeliveryPointSearchResult(**response)
		except ValidationError as e:
			logger.error(f"Validation error in search_delivery_points: {e}")
			raise
