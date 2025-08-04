# Examples

This document provides practical examples for common use cases with the CDEK Python SDK.

## Table of Contents

- [Basic Setup](#basic-setup)
- [Order Management](#order-management)
- [Tariff Calculations](#tariff-calculations)
- [Location Services](#location-services)
- [Courier Services](#courier-services)
- [Printing Services](#printing-services)
- [Webhook Management](#webhook-management)

## Basic Setup

```python
import asyncio
from aiocdek import CDEKAPIClient

# Initialize client
client = CDEKAPIClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    test_environment=False
)
```

## Order Management

### Creating a Simple Order

```python
from aiocdek.models import OrderRequest, OrderPackage, OrderSender, OrderRecipient, Location
from aiocdek.enums import TariffCode

async def create_simple_order():
    order = OrderRequest(
        type=1,  # Online store
        number="ORDER-12345",
        tariff_code=TariffCode.EXPRESS_DOOR_TO_DOOR,
        sender=OrderSender(
            name="Ivan Petrov",
            phones=["+79001234567"],
            email="sender@example.com"
        ),
        recipient=OrderRecipient(
            name="Anna Sidorova",
            phones=["+79009876543"],
            email="recipient@example.com"
        ),
        from_location=Location(
            address="Moscow, Tverskaya Street, 1"
        ),
        to_location=Location(
            address="St. Petersburg, Nevsky Prospect, 28"
        ),
        packages=[
            OrderPackage(
                number="PKG-001",
                weight=500,  # 500 grams
                length=20,   # 20 cm
                width=15,    # 15 cm
                height=5     # 5 cm
            )
        ]
    )
    
    result = await client.create_order(order)
    print(f"Order created with UUID: {result.entity.uuid}")
    return result
```

### Creating an Order with Items

```python
from aiocdek.models import OrderItem, Money
from aiocdek.enums import CountryCode

async def create_order_with_items():
    items = [
        OrderItem(
            name="T-shirt",
            ware_key="TSHIRT-001",
            payment=Money(value=1500, vat_sum=250),
            cost=1500.0,
            weight=200,
            amount=2,
            brand="MyBrand",
            country_code=CountryCode.RU
        ),
        OrderItem(
            name="Jeans",
            ware_key="JEANS-001", 
            payment=Money(value=3000, vat_sum=500),
            cost=3000.0,
            weight=800,
            amount=1,
            brand="MyBrand",
            country_code=CountryCode.RU
        )
    ]
    
    package = OrderPackage(
        number="PKG-001",
        weight=1200,  # Total weight
        items=items
    )
    
    order = OrderRequest(
        type=1,
        number="ORDER-WITH-ITEMS-001",
        tariff_code=TariffCode.EXPRESS_DOOR_TO_PICKUP,
        sender=OrderSender(
            name="Online Store LLC",
            phones=["+79001234567"],
            email="orders@store.com"
        ),
        recipient=OrderRecipient(
            name="Customer Name",
            phones=["+79009876543"]
        ),
        from_location=Location(code=270),  # Moscow
        to_location=Location(code=2),      # St. Petersburg
        packages=[package]
    )
    
    result = await client.create_order(order)
    return result
```

### Tracking Order Status

```python
async def track_order(order_uuid: str):
    order_info = await client.get_order(order_uuid)
    
    print(f"Order Number: {order_info.number}")
    print(f"Current Status: {order_info.statuses[-1].name}")
    print(f"Status Date: {order_info.statuses[-1].date_time}")
    
    # Print all status history
    print("\nStatus History:")
    for status in order_info.statuses:
        print(f"- {status.date_time}: {status.name}")
    
    return order_info
```

## Tariff Calculations

### Compare Multiple Tariffs

```python
from aiocdek.models import TariffListRequest

async def compare_tariffs():
    request = TariffListRequest(
        type=1,
        from_location=Location(code=270),  # Moscow
        to_location=Location(code=44),     # Ekaterinburg
        packages=[{
            "weight": 1000,
            "length": 30,
            "width": 20,
            "height": 15
        }]
    )
    
    tariffs = await client.calculate_tariff_list(request)
    
    print("Available tariffs:")
    for tariff in sorted(tariffs, key=lambda x: x.delivery_sum):
        print(f"Tariff {tariff.tariff_code}: {tariff.delivery_sum} RUB "
              f"({tariff.period_min}-{tariff.period_max} days)")
    
    return tariffs
```

### Calculate with Additional Services

```python
from aiocdek.models import Service

async def calculate_with_services():
    services = [
        Service(code="INSURANCE", parameter="5000"),  # Insurance for 5000 RUB
        Service(code="CALL", parameter="1"),          # Call recipient
    ]
    
    request = TariffRequest(
        type=1,
        from_location=Location(code=270),
        to_location=Location(code=44),
        packages=[{"weight": 1000}],
        services=services
    )
    
    tariff = await client.calculate_tariff(request)
    print(f"Base cost: {tariff.delivery_sum} RUB")
    
    for service in tariff.services:
        print(f"Service {service.code}: {service.sum} RUB")
    
    return tariff
```

## Location Services

### Find Cities by Name

```python
from aiocdek.models import CitySearchParams

async def find_cities(city_name: str):
    params = CitySearchParams(
        city=city_name,
        size=10
    )
    
    cities = await client.get_cities(params)
    
    print(f"Found {len(cities)} cities matching '{city_name}':")
    for city in cities:
        print(f"- {city.city} ({city.code}), {city.region}")
    
    return cities
```

### Find Delivery Points

```python
from cdek.models import DeliveryPointSearchParams

async def find_pickup_points(city_code: int):
    params = DeliveryPointSearchParams(
        city_code=city_code,
        type="PVZ",  # Pickup points
        have_cash_less=True,  # Accept card payments
        have_cash=True,       # Accept cash payments
        is_dressing_room=True # Have fitting room
    )
    
    points = await client.get_delivery_points(params)
    
    print(f"Found {len(points)} pickup points in city {city_code}:")
    for point in points[:5]:  # Show first 5
        print(f"- {point.name}")
        print(f"  Address: {point.location.address}")
        print(f"  Phone: {point.phones[0] if point.phones else 'N/A'}")
        print(f"  Work time: {point.work_time}")
        print()
    
    return points
```

## Courier Services

### Request Courier Pickup

```python
from aiocdek.models import CourierRequest
from datetime import datetime, timedelta

async def request_courier():
    # Schedule pickup for tomorrow
    pickup_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    request = CourierRequest(
        intake_date=pickup_date,
        intake_time_from="10:00",
        intake_time_to="18:00",
        sender=OrderSender(
            name="Company LLC",
            phones=["+79001234567"],
            email="pickup@company.com"
        ),
        from_location=Location(
            address="Moscow, Business Center, Office 101"
        ),
        need_call=True,
        comment="Please call before arrival"
    )
    
    result = await client.create_courier_request(request)
    print(f"Courier request created: {result.entity.uuid}")
    return result
```

## Printing Services

### Generate Order Label

```python
async def print_order_label(order_uuid: str):
    # Get PDF label
    pdf_data = await client.get_order_print(order_uuid, format="pdf")
    
    # Save to file
    with open(f"label_{order_uuid}.pdf", "wb") as f:
        f.write(pdf_data)
    
    print(f"Label saved as label_{order_uuid}.pdf")
    
    # Get PNG label (if needed)
    png_data = await client.get_order_print(order_uuid, format="png")
    with open(f"label_{order_uuid}.png", "wb") as f:
        f.write(png_data)
```

### Generate Barcode

```python
async def print_barcode(order_uuid: str):
    barcode_data = await client.get_barcode_print(order_uuid, format="pdf")
    
    with open(f"barcode_{order_uuid}.pdf", "wb") as f:
        f.write(barcode_data)
    
    print(f"Barcode saved as barcode_{order_uuid}.pdf")
```

## Webhook Management

### Setup Order Status Webhooks

```python
from aiocdek.models import WebhookRequest

async def setup_webhooks():
    # Create webhook for order status updates
    webhook = WebhookRequest(
        url="https://yoursite.com/cdek/webhook",
        type="ORDER_STATUS"
    )
    
    result = await client.create_webhook(webhook)
    print(f"Webhook created: {result.entity.uuid}")
    
    # List all webhooks
    webhooks = await client.get_webhooks()
    print(f"Total webhooks: {len(webhooks)}")
    
    for wh in webhooks:
        print(f"- {wh.type}: {wh.url}")
    
    return result
```

### Handle Webhook Data

```python
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/cdek/webhook', methods=['POST'])
def handle_cdek_webhook():
    data = request.get_json()
    
    # Process order status update
    if data.get('type') == 'ORDER_STATUS':
        order_uuid = data['attributes']['uuid']
        status = data['attributes']['status_code']
        
        print(f"Order {order_uuid} status changed to: {status}")
        
        # Update your database
        # update_order_status(order_uuid, status)
    
    return "OK", 200
```

## Complete Workflow Example

```python
async def complete_shipping_workflow():
    """Complete example: calculate, create order, track, and print label"""
    
    # 1. Calculate tariff
    tariff_request = TariffRequest(
        type=1,
        from_location=Location(code=270),  # Moscow
        to_location=Location(code=44),     # Ekaterinburg
        packages=[{"weight": 1000}]
    )
    
    tariff = await client.calculate_tariff(tariff_request)
    print(f"Delivery cost: {tariff.delivery_sum} RUB")
    
    # 2. Create order
    order = OrderRequest(
        type=1,
        number="WORKFLOW-001",
        tariff_code=tariff.tariff_code,
        sender=OrderSender(
            name="Sender Name",
            phones=["+79001234567"]
        ),
        recipient=OrderRecipient(
            name="Recipient Name",
            phones=["+79009876543"]
        ),
        from_location=Location(code=270),
        to_location=Location(code=44),
        packages=[OrderPackage(
            number="PKG-001",
            weight=1000
        )]
    )
    
    order_result = await client.create_order(order)
    order_uuid = order_result.entity.uuid
    print(f"Order created: {order_uuid}")
    
    # 3. Track order
    order_info = await client.get_order(order_uuid)
    print(f"Current status: {order_info.statuses[-1].name}")
    
    # 4. Generate label
    label_data = await client.get_order_print(order_uuid, format="pdf")
    with open(f"label_{order_uuid}.pdf", "wb") as f:
        f.write(label_data)
    print("Label generated successfully")
    
    return order_uuid

# Run the workflow
if __name__ == "__main__":
    asyncio.run(complete_shipping_workflow())
```
