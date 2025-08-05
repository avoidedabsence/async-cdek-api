import uuid

from pydantic import BaseModel, Field
from ..enums import CountryCode, Language


class RegionSearchParams(BaseModel):
	country_codes: list[CountryCode] | None = Field(None, description="Country codes")
	region_code: int | None = Field(None, description="Region code")
	size: int | None = Field(1000, description="Results per page")
	page: int | None = Field(0, description="Page number")
	lang: Language | None = Field(Language.RU, description="Language")


class CitySearchParams(BaseModel):
	country_codes: list[CountryCode] | None = Field(None, description="Country codes")
	region_code: int | None = Field(None, description="Region code")
	city_code: int | None = Field(None, description="City code")
	postal_code: str | None = Field(None, description="Postal code")
	city: str | None = Field(None, description="City name")
	fias_guid: str | None = Field(None, description="FIAS GUID")
	kladr_code: str | None = Field(None, description="KLADR code")
	size: int | None = Field(1000, description="Results per page")
	page: int | None = Field(0, description="Page number")
	lang: Language | None = Field(Language.RU, description="Language")


class Region(BaseModel):
	country_code: CountryCode = Field(..., description="Country code")
	country: str = Field(..., description="Country name")
	region: str = Field("", description="Region name")
	region_code: int = Field(..., description="Region code")


class City(BaseModel):
	country_code: CountryCode = Field(..., description="Country code")
	country: str | None = Field(None, description="Country name")
	region: str | None = Field(None, description="Region name")
	region_code: int | None = Field(None, description="Region code")
	city: str = Field(..., description="City name")
	city_code: int = Field(..., alias="code", description="City code")
	postal_code: str | None = Field(None, description="Postal code")
	fias_guid: str | None = Field(None, description="FIAS GUID")
	kladr_code: str | None = Field(None, description="KLADR code")
	longitude: float | None = Field(None, description="Longitude")
	latitude: float | None = Field(None, description="Latitude")
	time_zone: str | None = Field(None, description="Time zone")
	payment_limit: float | None = Field(None, description="Payment limit")

class CityFromSearch(BaseModel):
	city_uuid: uuid.UUID = Field(..., description="City UUID")
	code: int = Field(..., description="City code")
	full_name: str = Field(..., description="Full name of the city")
