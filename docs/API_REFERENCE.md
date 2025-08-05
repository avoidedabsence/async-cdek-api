from aiocdek.models.locations import CityFromSearchfrom aiocdek.enums import CountryCode

# API Reference

This document provides detailed information about all classes, methods, and models in the CDEK Python SDK.

## Table of Contents

- [Client](#client)
- [Models](#models)
- [Enums](#enums)
- [Exceptions](#exceptions)

## Client

### CDEKAPIClient

The main client class for interacting with the CDEK API.

```python
class CDEKAPIClient(
    APIClient,
    CalculatorMixin,
    OrdersMixin,
    LocationsMixin,
    DeliveryPointsMixin,
    CourierMixin,
    PrintingMixin,
    WebhooksMixin,
)
```

#### Initialization

```python
CDEKAPIClient(client_id: str, client_secret: str, test_environment: bool = False, debug: bool = False)
```

**Parameters:**
- `client_id` (str): Your CDEK API client ID
- `client_secret` (str): Your CDEK API client secret
- `test_environment` (bool): Default: False; If to use api.edu.cdek.ru as base_url for API
- `debug` (bool): Default: False; If to log every API request

#### Authentication

The client automatically handles OAuth authentication and token caching. Tokens are refreshed automatically when they expire.

## Order Management

### create_order

Create a new delivery order.

```python
async def create_order(order: OrderRequest) -> OrderResponse
```

**Parameters:**
- `order` (OrderRequest): Order details

**Returns:**
- `OrderResponse`: Created order information

**Example:**
```python
order = OrderRequest(
    type=1,
    number="ORDER-001",
    tariff_code=TariffCode.EXPRESS_DOOR_TO_DOOR,
    # ... other fields
)
result = await client.create_order(order)
```

### get_order

Get order information by UUID.

```python
async def get_order(uuid: str) -> OrderInfo
```

**Parameters:**
- `uuid` (str): Order UUID

**Returns:**
- `OrderInfo`: Order details and status

**Example:**
```python
order_info = await client.get_order(order_uuid)
```

## Tariff Calculation

### calculate_tariff

Calculate delivery cost for a single tariff.

```python
async def calculate_tariff(request: TariffRequest) -> TariffResponse
```

**Parameters:**
- `request` (TariffRequest): Calculation parameters

**Returns:**
- `TariffResponse`: Delivery cost and timing

### calculate_tariff_list

Calculate delivery costs for multiple tariffs.

```python
async def calculate_tariff_list(request: TariffListRequest) -> list[TariffResponse]
```

**Parameters:**
- `request` (TariffListRequest): Calculation parameters

**Returns:**
- `list[TariffResponse]`: List of available tariffs with costs

### calculate_customs_duty

Calculate customs duty for international shipments.

```python
async def calculate_customs_duty(request: CustomsDutyRequest) -> CustomsDutyResponse
```

## Location Services

### get_regions

Get list of regions.

```python
async def get_regions(params: RegionSearchParams | None = None) -> list[Region]
```

**Parameters:**
- `params` (RegionSearchParams, optional): Search parameters

**Returns:**
- `list[Region]`: List of regions

### get_cities

Get list of cities.

```python
async def get_cities(params: CitySearchParams | None = None) -> list[City]
```

**Parameters:**
- `params` (CitySearchParams, optional): Search parameters

**Returns:**
- `list[City]`: List of cities

### get_approximate_city

Get a list of cities approximate to query

```python
async def get_cities(query: str, country_code: CountryCode = CountryCode.RU) -> list[CityFromSearch]
```

**Parameters:**
- `query` (str): Search query
- `country_code` (CountryCode): Default: `RU`; Country, from which to search cities

**Returns:**
- `list[City]`: List of cities

## Delivery Points

### get_delivery_points

Get list of delivery points (pickup points, lockers, etc.).

```python
async def get_delivery_points(params: DeliveryPointSearchParams | None = None) -> list[DeliveryPoint]
```

**Parameters:**
- `params` (DeliveryPointSearchParams, optional): Search parameters

**Returns:**
- `list[DeliveryPoint]`: List of delivery points

## Courier Services

### create_courier_request

Request courier pickup.

```python
async def create_courier_request(request: CourierRequest) -> CourierResponse
```

**Parameters:**
- `request` (CourierRequest): Courier request details

**Returns:**
- `CourierResponse`: Courier request information

### get_courier_request

Get courier request information.

```python
async def get_courier_request(uuid: str) -> CourierInfo
```

## Printing Services

### get_order_print

Get order label for printing.

```python
async def get_order_print(uuid: str, format: str = "pdf") -> bytes
```

**Parameters:**
- `uuid` (str): Order UUID
- `format` (str): Format ("pdf" or "png")

**Returns:**
- `bytes`: Label data

### get_barcode_print

Get order barcode for printing.

```python
async def get_barcode_print(uuid: str, format: str = "pdf") -> bytes
```

**Parameters:**
- `uuid` (str): Order UUID
- `format` (str): Format ("pdf" or "png")

**Returns:**
- `bytes`: Barcode data

## Webhook Management

### create_webhook

Create a webhook subscription.

```python
async def create_webhook(webhook: WebhookRequest) -> WebhookResponse
```

**Parameters:**
- `webhook` (WebhookRequest): Webhook configuration

**Returns:**
- `WebhookResponse`: Created webhook information

### get_webhooks

Get list of webhooks.

```python
async def get_webhooks() -> list[WebhookInfo]
```

**Returns:**
- `list[WebhookInfo]`: List of configured webhooks

### delete_webhook

Delete a webhook.

```python
async def delete_webhook(uuid: str) -> bool
```

**Parameters:**
- `uuid` (str): Webhook UUID

**Returns:**
- `bool`: Success status

## Models

### Order Models

#### OrderRequest

Model for creating orders.

```python
class OrderRequest(BaseModel):
    type: int                           # Order type (1=online store, 2=regular)
    number: str                         # Your order number
    tariff_code: TariffCode            # Delivery tariff
    comment: str | None = None         # Order comment
    developer_key: str | None = None   # Developer key
    shipment_point: str | None = None  # Shipment point code
    delivery_point: str | None = None  # Delivery point code
    date_invoice: str | None = None    # Invoice date
    shipper_name: str | None = None    # Shipper name
    shipper_address: str | None = None # Shipper address
    delivery_recipient_cost: Money | None = None  # COD amount
    delivery_recipient_cost_adv: list[Money] | None = None
    sender: OrderSender                # Sender information
    recipient: OrderRecipient          # Recipient information
    from_location: Location            # Origin location
    to_location: Location              # Destination location
    services: list[Service] | None = None  # Additional services
    packages: list[OrderPackage]      # Package information
```

#### OrderPackage

Model for package information.

```python
class OrderPackage(BaseModel):
    number: str                        # Package number
    weight: int                        # Weight in grams
    length: int | None = None          # Length in cm
    width: int | None = None           # Width in cm
    height: int | None = None          # Height in cm
    comment: str | None = None         # Package comment
    items: list[OrderItem] | None = None  # Items in package
```

#### OrderItem

Model for items in packages.

```python
class OrderItem(BaseModel):
    name: str                          # Item name
    ware_key: str                      # Item identifier
    payment: Money                     # Item cost
    cost: float                        # Declared value
    weight: int                        # Weight in grams
    amount: int                        # Quantity
    name_i18n: str | None = None       # Item name in English
    brand: str | None = None           # Brand
    country_code: CountryCode | None = None  # Country of origin
    material: int | None = None        # Material code
    wifi_gsm: bool | None = None       # Contains WiFi/GSM
    url: str | None = None             # Product URL
```

#### OrderSender / OrderRecipient

Models for sender and recipient information.

```python
class OrderSender(BaseModel):
    company: str | None = None         # Company name
    name: str                          # Person name
    email: str | None = None           # Email
    phones: list[str]                  # Phone numbers
    passport_series: str | None = None # Passport series
    passport_number: str | None = None # Passport number
    passport_date_of_issue: str | None = None  # Issue date
    passport_organization: str | None = None   # Issuing org
    tin: str | None = None             # Tax ID
    passport_date_of_birth: str | None = None  # Birth date
```

### Tariff Models

#### TariffRequest

Model for tariff calculation requests.

```python
class TariffRequest(BaseModel):
    type: int                          # Shipment type
    from_location: Location            # Origin location
    to_location: Location              # Destination location
    packages: list[dict]               # Package dimensions
    services: list[Service] | None = None  # Additional services
    tariff_code: TariffCode | None = None  # Specific tariff
```

#### TariffResponse

Model for tariff calculation results.

```python
class TariffResponse(BaseModel):
    tariff_code: int                   # Tariff code
    tariff_name: str                   # Tariff name
    tariff_description: str            # Description
    delivery_mode: DeliveryMode        # Delivery mode
    delivery_sum: float                # Delivery cost
    period_min: int                    # Min delivery days
    period_max: int                    # Max delivery days
    calendar_min: int | None = None    # Min calendar days
    calendar_max: int | None = None    # Max calendar days
    services: list[Service] | None = None  # Service costs
```

### Location Models

#### Location

Model for locations (addresses, cities, etc.).

```python
class Location(BaseModel):
    code: int | None = None            # Location code
    fias_guid: str | None = None       # FIAS GUID
    postal_code: str | None = None     # Postal code
    longitude: float | None = None     # Longitude
    latitude: float | None = None      # Latitude
    country_code: str | None = None    # Country code
    region: str | None = None          # Region name
    region_code: int | None = None     # Region code
    sub_region: str | None = None      # Sub-region
    city: str | None = None            # City name
    kladr_code: str | None = None      # KLADR code
    address: str | None = None         # Full address
```

#### City

Model for city information.

```python
class City(BaseModel):
    code: int                          # City code
    city: str                          # City name
    fias_guid: str | None = None       # FIAS GUID
    kladr_code: str | None = None      # KLADR code
    country_code: str                  # Country code
    country: str                       # Country name
    region: str                        # Region name
    region_code: int                   # Region code
    sub_region: str | None = None      # Sub-region
    longitude: float | None = None     # Longitude
    latitude: float | None = None      # Latitude
    time_zone: str | None = None       # Time zone
    payment_limit: float | None = None # Payment limit
```

### Base Models

#### Money

Model for monetary amounts.

```python
class Money(BaseModel):
    value: float                       # Amount
    vat_sum: float | None = None       # VAT amount
    vat_rate: int | None = None        # VAT rate
```

#### Service

Model for additional services.

```python
class Service(BaseModel):
    code: str                          # Service code
    parameter: str | None = None       # Service parameter
    sum: float | None = None           # Service cost
```

## Enums

### TariffCode

Available delivery tariff codes.

```python
class TariffCode(IntEnum):
    EXPRESS_DOOR_TO_DOOR = 1           # Express door-to-door
    EXPRESS_DOOR_TO_PICKUP = 2         # Express door-to-pickup
    EXPRESS_PICKUP_TO_DOOR = 3         # Express pickup-to-door
    EXPRESS_PICKUP_TO_PICKUP = 4       # Express pickup-to-pickup
    ECONOMY_DOOR_TO_DOOR = 5           # Economy door-to-door
    ECONOMY_DOOR_TO_PICKUP = 6         # Economy door-to-pickup
    ECONOMY_PICKUP_TO_DOOR = 7         # Economy pickup-to-door
    ECONOMY_PICKUP_TO_PICKUP = 8       # Economy pickup-to-pickup
    SUPER_EXPRESS_9_18 = 10            # Super express 9-18
    SUPER_EXPRESS_10_16 = 11           # Super express 10-16
    SUPER_EXPRESS_18_20 = 12           # Super express 18-20
    OVERNIGHT_EXPRESS = 15             # Overnight express
    ECONOMY_EXPRESS = 16               # Economy express
    # ... and many more
```

### OrderType

Order types.

```python
class OrderType(IntEnum):
    ONLINE_STORE = 1                   # Online store order
    REGULAR_DELIVERY = 2               # Regular delivery
```

### DeliveryMode

Delivery modes.

```python
class DeliveryMode(StrEnum):
    DOOR = "door"                      # Door delivery
    PICKUP = "pickup"                  # Pickup point delivery
```

### CountryCode

ISO country codes.

```python
class CountryCode(StrEnum):
    RU = "RU"                          # Russia
    BY = "BY"                          # Belarus
    KZ = "KZ"                          # Kazakhstan
    KG = "KG"                          # Kyrgyzstan
    AM = "AM"                          # Armenia
    # ... and more
```

## Service Codes

Common additional service codes:

- `INSURANCE` - Cargo insurance
- `CALL` - Call recipient
- `PART_DELIVERY` - Partial delivery
- `CARGO_CHECK` - Cargo checking
- `DANGEROUS` - Dangerous goods
- `TRYING_ON` - Trying on clothes
- `REVERSE` - Reverse delivery
- `SMS` - SMS notifications
- `PHOTO_DOCUMENT` - Photo documents

