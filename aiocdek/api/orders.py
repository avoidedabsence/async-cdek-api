from pydantic import ValidationError
from loguru import logger
from ..models import (
	OrderRequest,
	OrderResponse,
	OrderInfo,
	OrderSearchParams,
)


class OrdersMixin:
	@classmethod
	async def create_order(cls, order: OrderRequest) -> OrderResponse:
		try:
			response = await cls._post(
				"/v2/orders", json=order.model_dump(exclude_none=True)
			)
			return OrderResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in create_order: {e}")
			raise

	@classmethod
	async def get_order(cls, uuid: str) -> OrderInfo:
		try:
			response = await cls._get(f"/v2/orders/{uuid}")
			return OrderInfo(**response)
		except ValidationError as e:
			logger.error(f"Validation error in get_order: {e}")
			raise

	@classmethod
	async def get_order_by_cdek_number(cls, cdek_number: str) -> list[OrderInfo]:
		try:
			response = await cls._get("/v2/orders", params={"cdek_number": cdek_number})
			if isinstance(response, list):
				return [OrderInfo(**order) for order in response]
			return [OrderInfo(**response)]
		except ValidationError as e:
			logger.error(f"Validation error in get_order_by_cdek_number: {e}")
			raise

	@classmethod
	async def get_orders(
		cls, params: OrderSearchParams | None = None
	) -> list[OrderInfo]:
		try:
			search_params = params.model_dump(exclude_none=True) if params else {}
			response = await cls._get("/v2/orders", params=search_params)
			if isinstance(response, list):
				return [OrderInfo(**order) for order in response]
			return [OrderInfo(**response)]
		except ValidationError as e:
			logger.error(f"Validation error in get_orders: {e}")
			raise

	@classmethod
	async def update_order(cls, uuid: str, order: OrderRequest) -> OrderResponse:
		try:
			response = await cls._put(
				f"/v2/orders/{uuid}", json=order.model_dump(exclude_none=True)
			)
			return OrderResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in update_order: {e}")
			raise

	@classmethod
	async def delete_order(cls, uuid: str) -> OrderResponse:
		try:
			response = await cls._delete(f"/v2/orders/{uuid}")
			return OrderResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in delete_order: {e}")
			raise
