from pydantic import BaseModel, Field
from . import Location, Service, CDEKError
from ..enums import TariffCode, Currency, Language, DeliveryMode


class CalculatorPackage(BaseModel):
	weight: int = Field(..., description="Total weight in grams", gt=0)
	length: int | None = Field(None, description="Length in centimeters", gt=0)
	width: int | None = Field(None, description="Width in centimeters", gt=0)
	height: int | None = Field(None, description="Height in centimeters", gt=0)
	volume_weight: int | None = Field(
		None, description="Volume weight (auto-calculated if not specified)"
	)


class TariffRequest(BaseModel):
	tariff_code: TariffCode | None = Field(None, description="Tariff code")
	from_location: Location = Field(..., description="Origin location")
	to_location: Location = Field(..., description="Destination location")
	packages: list[CalculatorPackage] = Field(
		..., description="Packages list", min_items=1
	)
	services: list[Service] | None = Field(None, description="Additional services")
	date: str | None = Field(None, description="Planned shipment date (YYYY-MM-DD)")
	currency: Currency | None = Field(
		Currency.RUB, description="Currency for calculation"
	)
	lang: Language | None = Field(
		Language.RU, description="Language for tariff information output"
	)


class TariffServiceResponse(BaseModel):
	code: str = Field(..., description="Service code")
	name: str = Field(..., description="Service name")
	sum: float = Field(..., description="Service cost")


class TariffResponse(BaseModel):
	tariff_code: TariffCode = Field(..., description="Tariff code")
	tariff_name: str = Field(..., description="Tariff name")
	tariff_description: str = Field(..., description="Tariff description")
	delivery_mode: DeliveryMode = Field(..., description="Tariff mode")
	delivery_sum: float = Field(..., description="Delivery cost")
	period_min: int = Field(..., description="Minimum delivery time in days")
	period_max: int = Field(..., description="Maximum delivery time in days")
	weight_calc: int = Field(..., description="Calculated weight in grams")
	total_sum: float = Field(..., description="Total cost")
	currency: Currency = Field(..., description="Currency")
	services: list[TariffServiceResponse] | None = Field(None, description="Services")
	errors: list[CDEKError] | None = Field(None, description="Errors")


class TariffListRequest(BaseModel):
	from_location: Location = Field(..., description="Origin location")
	to_location: Location = Field(..., description="Destination location")
	packages: list[CalculatorPackage] = Field(
		..., description="Packages list", min_items=1
	)
	services: list[Service] | None = Field(None, description="Additional services")
	date: str | None = Field(None, description="Planned shipment date (YYYY-MM-DD)")
	currency: Currency | None = Field(
		Currency.RUB, description="Currency for calculation"
	)
	lang: Language | None = Field(
		Language.RU, description="Language for tariff information output"
	)


class CustomsDutyRequest(BaseModel):
	from_location: Location = Field(..., description="Origin location")
	to_location: Location = Field(..., description="Destination location")
	packages: list[CalculatorPackage] = Field(
		..., description="Packages list", min_items=1
	)
	currency: Currency | None = Field(
		Currency.RUB, description="Currency for calculation"
	)


class CustomsDutyResponse(BaseModel):
	duty_sum: float = Field(..., description="Customs duty amount")
	vat_sum: float = Field(..., description="VAT amount")
	total_sum: float = Field(..., description="Total customs payments")
	currency: Currency = Field(..., description="Currency")
	errors: list[CDEKError] | None = Field(None, description="Errors")
