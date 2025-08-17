from pydantic import ValidationError
from loguru import logger
from ..models import (
	CourierRequest,
	CourierResponse,
	CourierInfo,
	CourierSearchParams,
)


class CourierMixin:
	async def create_courier_request(self, request: CourierRequest) -> CourierResponse:
		try:
			response = await self._post(
				"/v2/intakes", json=request.model_dump(exclude_none=True)
			)
			return CourierResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in create_courier_request: {e}")
			raise

	async def get_courier_request(self, uuid: str) -> CourierInfo:
		try:
			response = await self._get(f"/v2/intakes/{uuid}")
			return CourierInfo(**response)
		except ValidationError as e:
			logger.error(f"Validation error in get_courier_request: {e}")
			raise

	async def get_courier_requests(
		self, params: CourierSearchParams | None = None
	) -> list[CourierInfo]:
		try:
			search_params = params.model_dump(exclude_none=True) if params else {}
			response = await self._get("/v2/intakes", params=search_params)
			if isinstance(response, list):
				return [CourierInfo(**request) for request in response]
			return [CourierInfo(**response)]
		except ValidationError as e:
			logger.error(f"Validation error in get_courier_requests: {e}")
			raise

	async def delete_courier_request(self, uuid: str) -> CourierResponse:
		try:
			response = await self._delete(f"/v2/intakes/{uuid}")
			return CourierResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in delete_courier_request: {e}")
			raise
