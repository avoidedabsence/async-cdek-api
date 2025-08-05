from pydantic import ValidationError
from loguru import logger
from ..models import (
	TariffRequest,
	TariffResponse,
	TariffListRequest,
	CustomsDutyRequest,
	CustomsDutyResponse,
)


class CalculatorMixin:
	@classmethod
	async def calculate_tariff(cls, request: TariffRequest) -> TariffResponse:
		try:
			response = await cls._post(
				"/v2/calculator/tariff", json=request.model_dump(exclude_none=True)
			)
			return TariffResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in calculate_tariff: {e}")
			raise

	@classmethod
	async def calculate_tariff_list(
		cls, request: TariffListRequest
	) -> list[TariffResponse]:
		try:
			response = await cls._post(
				"/v2/calculator/tarifflist", json=request.model_dump(exclude_none=True)
			)
			tariff_codes = response.get("tariff_codes", [])
			return [TariffResponse(**tariff) for tariff in tariff_codes]
		except ValidationError as e:
			logger.error(f"Validation error in calculate_tariff_list: {e}")
			raise

	@classmethod
	async def calculate_customs_duty(
		cls, request: CustomsDutyRequest
	) -> CustomsDutyResponse:
		try:
			response = await cls._post(
				"/v2/calculator/customs-duty",
				json=request.model_dump(exclude_none=True),
			)
			return CustomsDutyResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in calculate_customs_duty: {e}")
			raise
