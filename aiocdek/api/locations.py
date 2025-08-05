from pydantic import ValidationError
from loguru import logger

from ..enums import CountryCode
from ..models import (
	RegionSearchParams,
	CitySearchParams,
	Region,
	City,
)
from ..models.locations import CityFromSearch


class LocationsMixin:
    @classmethod
    async def get_regions(
        cls, params: RegionSearchParams | None = None
    ) -> list[Region]:
        try:
            search_params = (
                params.model_dump(exclude_none=True)
                if params
                else {"size": 1000, "page": 0}
            )
            response = await cls._get("/v2/location/regions", params=search_params)
            if isinstance(response, list):
                return [Region(**region) for region in response]
            return [Region(**response)]
        except ValidationError as e:
            logger.error(f"Validation error in get_regions: {e}")
            raise

    @classmethod
    async def get_cities(cls, params: CitySearchParams | None = None) -> list[City]:
        try:
            search_params = (
                params.model_dump(exclude_none=True)
                if params
                else {"size": 1000, "page": 0}
            )
            response = await cls._get("/v2/location/cities", params=search_params)
            if isinstance(response, list):
                return [City(**city) for city in response]
            return [City(**response)]
        except ValidationError as e:
            logger.error(f"Validation error in get_cities: {e}")
            raise

    @classmethod
    async def get_approximate_city(cls, query: str, country_code: CountryCode = CountryCode.RU) -> list[CityFromSearch]:
        try:

            response = await cls._get(
                "/v2/location/suggest/cities", params={
                    "name": query,
                    "country_code": country_code
                }
            )
            if isinstance(response, list):
                return [CityFromSearch(**city) for city in response]
            return [CityFromSearch(**response)]
        except ValidationError as e:
            logger.error(f"Validation error in get_approximate_cities: {e}")
            raise
