# pycdek

pycdek is an asynchronous Python client for the CDEK API. It allows you to interact with the CDEK service using Python's async capabilities for non-blocking operations.

## Features
- Fully asynchronous API client
- Easy integration with Python applications
- Supports all major CDEK API endpoints

## Installation
```
pip install pycdek
```

## Usage Example
```python
import asyncio
from pycdek import CDEKClient

async def main():
    client = CDEKClient(api_key="YOUR_API_KEY")
    result = await client.get_order(order_id="123456")
    print(result)

asyncio.run(main())
```

## Documentation
Refer to the official CDEK API documentation for details on available endpoints and parameters: https://api.cdek.ru/

## License
MIT