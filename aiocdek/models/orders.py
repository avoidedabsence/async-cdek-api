from pydantic import BaseModel, Field
from . import Location, Service, CDEKError, Money
from ..enums import OrderType, TariffCode, DeliveryMode, CountryCode


class OrderPackage(BaseModel):
	number: str = Field(..., description="Package number")
	weight: int = Field(..., description="Weight in grams", gt=0)
	length: int | None = Field(None, description="Length in centimeters")
	width: int | None = Field(None, description="Width in centimeters")
	height: int | None = Field(None, description="Height in centimeters")
	comment: str | None = Field(None, description="Package comment")
	items: list["OrderItem"] | None = Field(None, description="Items in package")


class OrderItem(BaseModel):
	name: str = Field(..., description="Item name")
	ware_key: str = Field(..., description="Item identifier")
	payment: Money = Field(..., description="Item cost")
	cost: float = Field(..., description="Declared value")
	weight: int = Field(..., description="Weight in grams")
	amount: int = Field(..., description="Quantity")
	name_i18n: str | None = Field(None, description="Item name in English")
	brand: str | None = Field(None, description="Brand")
	country_code: CountryCode | None = Field(None, description="Country of origin code")
	material: int | None = Field(None, description="Material code")
	wifi_gsm: bool | None = Field(None, description="Contains WiFi/GSM")
	url: str | None = Field(None, description="Product URL")


class OrderSender(BaseModel):
	company: str | None = Field(None, description="Company name")
	name: str = Field(..., description="Sender name")
	email: str | None = Field(None, description="Email")
	phones: list[str] = Field(..., description="Phone numbers")
	passport_series: str | None = Field(None, description="Passport series")
	passport_number: str | None = Field(None, description="Passport number")
	passport_date_of_issue: str | None = Field(None, description="Passport issue date")
	passport_organization: str | None = Field(
		None, description="Passport issuing organization"
	)
	tin: str | None = Field(None, description="Tax identification number")
	passport_date_of_birth: str | None = Field(None, description="Date of birth")


class OrderRecipient(BaseModel):
	company: str | None = Field(None, description="Company name")
	name: str = Field(..., description="Recipient name")
	email: str | None = Field(None, description="Email")
	phones: list[str] = Field(..., description="Phone numbers")
	passport_series: str | None = Field(None, description="Passport series")
	passport_number: str | None = Field(None, description="Passport number")
	passport_date_of_issue: str | None = Field(None, description="Passport issue date")
	passport_organization: str | None = Field(
		None, description="Passport issuing organization"
	)
	tin: str | None = Field(None, description="Tax identification number")
	passport_date_of_birth: str | None = Field(None, description="Date of birth")


class OrderRequest(BaseModel):
	type: OrderType = Field(
		..., description="Order type: 1 - online store, 2 - regular delivery"
	)
	number: str = Field(..., description="Order number")
	tariff_code: TariffCode = Field(..., description="Tariff code")
	comment: str | None = Field(None, description="Order comment")
	developer_key: str | None = Field(None, description="Developer key")
	shipment_point: str | None = Field(None, description="Shipment point code")
	delivery_point: str | None = Field(None, description="Delivery point code")
	date_invoice: str | None = Field(None, description="Invoice date")
	shipper_name: str | None = Field(None, description="Shipper name")
	shipper_address: str | None = Field(None, description="Shipper address")
	delivery_recipient_cost: Money | None = Field(
		None, description="Delivery cost paid by recipient"
	)
	delivery_recipient_cost_adv: list[Money] | None = Field(
		None, description="Additional delivery costs"
	)
	from_location: Location = Field(..., description="Origin location")
	to_location: Location = Field(..., description="Destination location")
	packages: list[OrderPackage] = Field(..., description="Packages", min_items=1)
	sender: OrderSender = Field(..., description="Sender information")
	recipient: OrderRecipient = Field(..., description="Recipient information")
	services: list[Service] | None = Field(None, description="Additional services")


class OrderResponse(BaseModel):
	entity: dict = Field(..., description="Created/updated order entity")
	requests: list[dict] | None = Field(None, description="Related requests")


class OrderInfo(BaseModel):
	uuid: str = Field(..., description="Order UUID")
	type: OrderType = Field(..., description="Order type")
	number: str = Field(..., description="Order number")
	tariff_code: TariffCode = Field(..., description="Tariff code")
	tariff_name: str = Field(..., description="Tariff name")
	tariff_description: str = Field(..., description="Tariff description")
	delivery_mode: DeliveryMode = Field(..., description="Delivery mode")
	delivery_detail: dict = Field(..., description="Delivery details")
	from_location: Location = Field(..., description="Origin location")
	to_location: Location = Field(..., description="Destination location")
	packages: list[OrderPackage] = Field(..., description="Packages")
	sender: OrderSender = Field(..., description="Sender information")
	recipient: OrderRecipient = Field(..., description="Recipient information")
	services: list[Service] | None = Field(None, description="Additional services")
	statuses: list[dict] | None = Field(None, description="Order statuses")
	calls: list[dict] | None = Field(None, description="Delivery calls")
	errors: list[CDEKError] | None = Field(None, description="Errors")


class OrderSearchParams(BaseModel):
	cdek_number: str | None = Field(None, description="CDEK order number")
	im_number: str | None = Field(None, description="IM number")
	order_uuid: str | None = Field(None, description="Order UUID")
	date_first: str | None = Field(None, description="Start date filter")
	date_last: str | None = Field(None, description="End date filter")
	size: int | None = Field(1000, description="Results per page")
	page: int | None = Field(0, description="Page number")
