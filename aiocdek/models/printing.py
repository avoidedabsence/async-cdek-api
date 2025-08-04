from pydantic import BaseModel, Field
from ..enums import PrintFormat


class PrintRequest(BaseModel):
	orders: list[str] = Field(..., description="List of order UUIDs")
	format: PrintFormat = Field(PrintFormat.A4, description="Print format")

	def to_query_params(self) -> dict:
		return {"orders": ",".join(self.orders), "format": self.format}


class PrintResponse(BaseModel):
	uuid: str = Field(..., description="Print job UUID")
	url: str | None = Field(None, description="Download URL for print file")
	statuses: list[dict] | None = Field(None, description="Print job statuses")
	errors: list[dict] | None = Field(None, description="Print job errors")
