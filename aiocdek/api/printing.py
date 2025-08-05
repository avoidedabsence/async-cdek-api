from pydantic import ValidationError
from loguru import logger

from ..enums import PrintFormat
from ..models import (
	PrintRequest,
	PrintResponse,
)


class PrintingMixin:
	@classmethod
	async def get_order_print_form(
		cls, order_uuids: list[str], format: PrintFormat = PrintFormat.A4
	) -> PrintResponse:
		try:
			print_request = PrintRequest(orders=order_uuids, format=format)
			response = await cls._get(
				"/v2/print/orders", params=print_request.to_query_params()
			)
			return PrintResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in get_order_print_form: {e}")
			raise

	@classmethod
	async def get_order_barcode(
		cls, order_uuids: list[str], format: PrintFormat = PrintFormat.A4
	) -> PrintResponse:
		try:
			print_request = PrintRequest(orders=order_uuids, format=format)
			response = await cls._get(
				"/v2/print/barcodes", params=print_request.to_query_params()
			)
			return PrintResponse(**response)
		except ValidationError as e:
			logger.error(f"Validation error in get_order_barcode: {e}")
			raise
