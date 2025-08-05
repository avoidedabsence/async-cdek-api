from pydantic import ValidationError
from loguru import logger
from ..models import (
	CourierRequest,
	CourierResponse,
	CourierInfo,
	CourierSearchParams,
)


class CourierMixin:
	@classmethod
	async def create_courier_request(cls, request: CourierRequest) -> CourierResponse:
		try:
			response = await cls._post(
				"/v2/intakes", json=request.model_dump(exclude_none=True)
			)
			return CourierResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in create_courier_request: {e}")
			raise

	@classmethod
	async def get_courier_request(cls, uuid: str) -> CourierInfo:
		try:
			response = await cls._get(f"/v2/intakes/{uuid}")
			return CourierInfo(**response)
		except ValidationError as e:
			logger.error(f"Validation error in get_courier_request: {e}")
			raise

	@classmethod
	async def get_courier_requests(
		cls, params: CourierSearchParams | None = None
	) -> list[CourierInfo]:
		try:
			search_params = params.model_dump(exclude_none=True) if params else {}
			response = await cls._get("/v2/intakes", params=search_params)
			if isinstance(response, list):
				return [CourierInfo(**request) for request in response]
			return [CourierInfo(**response)]
		except ValidationError as e:
			logger.error(f"Validation error in get_courier_requests: {e}")
			raise

	@classmethod
	async def delete_courier_request(cls, uuid: str) -> CourierResponse:
		try:
			response = await cls._delete(f"/v2/intakes/{uuid}")
			return CourierResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in delete_courier_request: {e}")
			raise
