from pydantic import BaseModel, Field
from ..enums import DeliveryPointType, CountryCode, Language


class DeliveryPointFilter(BaseModel):
	postal_code: str | None = Field(None, description="Postal code")
	city_code: int | None = Field(None, description="City code")
	type: DeliveryPointType | None = Field(
		None, description="Point type (PVZ, POSTAMAT)"
	)
	country_code: CountryCode | None = Field(None, description="Country code")
	region_code: int | None = Field(None, description="Region code")
	have_cashless: bool | None = Field(None, description="Cashless payment available")
	have_cash: bool | None = Field(None, description="Cash payment available")
	allowed_cod: bool | None = Field(None, description="Cash on delivery allowed")
	is_dressing_room: bool | None = Field(None, description="Has dressing room")
	weight_max: int | None = Field(None, description="Maximum weight limit")
	lang: Language | None = Field(Language.RU, description="Language")
	take_only: bool | None = Field(None, description="Take only (no reception)")


class WorkTime(BaseModel):
	day: int = Field(..., description="Day of week (1-7)")
	time: str = Field(..., description="Working hours (HH:MM-HH:MM)")


class DeliveryPoint(BaseModel):
	code: str = Field(..., description="Point code")
	name: str = Field(..., description="Point name")
	uuid: str | None = Field(None, description="Point UUID")
	location: dict = Field(..., description="Location information")
	address_comment: str | None = Field(None, description="Address comment")
	nearest_station: str | None = Field(None, description="Nearest metro station")
	nearest_metro_station: str | None = Field(None, description="Nearest metro station")
	work_time: str | None = Field(None, description="Working hours")
	work_time_list: list[WorkTime] | None = Field(
		None, description="Detailed working hours"
	)
	work_time_exceptions: list[dict] | None = Field(
		None, description="Working hours exceptions"
	)
	phones: list[dict] | None = Field(None, description="Phone numbers")
	email: str | None = Field(None, description="Email")
	note: str | None = Field(None, description="Additional notes")
	type: DeliveryPointType = Field(..., description="Point type")
	owner_code: str | None = Field(None, description="Owner code")
	take_only: bool = Field(..., description="Take only (no reception)")
	is_handout: bool = Field(..., description="Is handout point")
	is_reception: bool = Field(..., description="Is reception point")
	is_dressing_room: bool = Field(..., description="Has dressing room")
	have_cashless: bool = Field(..., description="Cashless payment available")
	have_cash: bool = Field(..., description="Cash payment available")
	allowed_cod: bool = Field(..., description="Cash on delivery allowed")
	site: str | None = Field(None, description="Website")
	weight_min: int | None = Field(None, description="Minimum weight limit")
	weight_max: int | None = Field(None, description="Maximum weight limit")
	fulfillment: bool | None = Field(None, description="Fulfillment available")


class DeliveryPointSearchResult(BaseModel):
	points: list[DeliveryPoint] = Field(..., description="Delivery points")
	total: int | None = Field(None, description="Total points count")
