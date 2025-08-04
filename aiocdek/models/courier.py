from pydantic import BaseModel, Field
from . import Location, Contact
from ..enums import WeightLimit, DimensionLimit


class CourierRequest(BaseModel):
	intake_date: str = Field(..., description="Pickup date (YYYY-MM-DD)")
	intake_time_from: str = Field(..., description="Pickup time from (HH:MM)")
	intake_time_to: str = Field(..., description="Pickup time to (HH:MM)")
	lunch_time_from: str | None = Field(None, description="Lunch break from (HH:MM)")
	lunch_time_to: str | None = Field(None, description="Lunch break to (HH:MM)")
	name: str = Field(..., description="Contact name")
	weight: int = Field(
		..., description="Total weight in grams", ge=WeightLimit.MIN_WEIGHT
	)
	length: int | None = Field(
		None, description="Length in centimeters", ge=DimensionLimit.MIN_DIMENSION
	)
	width: int | None = Field(
		None, description="Width in centimeters", ge=DimensionLimit.MIN_DIMENSION
	)
	height: int | None = Field(
		None, description="Height in centimeters", ge=DimensionLimit.MIN_DIMENSION
	)
	comment: str | None = Field(None, description="Comment")
	from_location: Location = Field(..., description="Pickup location")
	sender: Contact = Field(..., description="Sender contact information")
	need_call: bool | None = Field(None, description="Need to call before pickup")


class CourierResponse(BaseModel):
	entity: dict = Field(..., description="Created courier request entity")
	requests: list[dict] | None = Field(None, description="Related requests")


class CourierInfo(BaseModel):
	uuid: str = Field(..., description="Request UUID")
	intake_number: str | None = Field(None, description="Intake number")
	intake_date: str = Field(..., description="Pickup date")
	intake_time_from: str = Field(..., description="Pickup time from")
	intake_time_to: str = Field(..., description="Pickup time to")
	lunch_time_from: str | None = Field(None, description="Lunch break from")
	lunch_time_to: str | None = Field(None, description="Lunch break to")
	name: str = Field(..., description="Contact name")
	weight: int = Field(..., description="Total weight")
	length: int | None = Field(None, description="Length")
	width: int | None = Field(None, description="Width")
	height: int | None = Field(None, description="Height")
	comment: str | None = Field(None, description="Comment")
	from_location: Location = Field(..., description="Pickup location")
	sender: Contact = Field(..., description="Sender contact information")
	statuses: list[dict] | None = Field(None, description="Request statuses")


class CourierSearchParams(BaseModel):
	intake_number: str | None = Field(None, description="Intake number")
	date_first: str | None = Field(None, description="Start date filter")
	date_last: str | None = Field(None, description="End date filter")
	size: int | None = Field(1000, description="Results per page")
	page: int | None = Field(0, description="Page number")
