from pydantic import BaseModel, Field
from ..enums import CountryCode, ServiceCode, Currency, VATRate


class Coordinates(BaseModel):
	latitude: float = Field(..., description="Latitude")
	longitude: float = Field(..., description="Longitude")


class Location(BaseModel):
	code: int | None = Field(None, description="City code from CDEK database")
	postal_code: str | None = Field(None, description="Postal code")
	country_code: CountryCode | None = Field(
		None, description="Country code in ISO_3166-1_alpha-2 format"
	)
	region: str | None = Field(None, description="Region name")
	region_code: int | None = Field(None, description="Region code")
	city: str | None = Field(None, description="City name")
	fias_guid: str | None = Field(None, description="FIAS code")
	kladr_code: str | None = Field(None, description="KLADR code")
	address: str | None = Field(None, description="Street address")


class Service(BaseModel):
	code: ServiceCode = Field(..., description="Service code")
	parameter: str | None = Field(None, description="Service parameter")


class CDEKError(BaseModel):
	code: str = Field(..., description="Error code")
	message: str = Field(..., description="Error message")


class Money(BaseModel):
	value: float = Field(..., description="Amount value")
	vat_sum: float | None = Field(None, description="VAT amount")
	vat_rate: VATRate | None = Field(None, description="VAT rate")
	currency: Currency | None = Field(None, description="Currency code")


class Contact(BaseModel):
	name: str = Field(..., description="Contact name")
	phones: list[str] = Field(..., description="Phone numbers")
	email: str | None = Field(None, description="Email address")
	passport_series: str | None = Field(None, description="Passport series")
	passport_number: str | None = Field(None, description="Passport number")
	passport_date_of_issue: str | None = Field(None, description="Passport issue date")
	passport_organization: str | None = Field(
		None, description="Passport issuing organization"
	)
	tin: str | None = Field(None, description="Tax identification number")
	passport_date_of_birth: str | None = Field(None, description="Date of birth")
