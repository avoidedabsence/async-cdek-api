import re
import sys
from contextlib import asynccontextmanager
from typing import Literal

import aiohttp.client_exceptions
from aiohttp import ClientSession
from loguru import logger


class APIClient:
    _base_url: str = None
    _client_name: str = __qualname__
    _debug_mode: bool = False

    @classmethod
    @asynccontextmanager
    async def _get_cached_auth_data(cls):
        yield

    @classmethod
    async def _request(
        cls,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        path: str,
        params: dict = None,
        json: dict = None,
        **kwargs,
    ):
        async with (
            cls._get_cached_auth_data() as auth,
            ClientSession(base_url=cls._base_url) as client,
        ):
            assert path.startswith("/"), "invalid request path"
            assert re.match(r"^(https:|http:|\.)\S*", cls._base_url), (
                f"invalid base_url for {cls._client_name}"
            )

            headers = None

            if auth is not None:
                headers = {"Authorization": f"Bearer {auth.access_token}"}

            request = await client.request(
                method=method,
                url=path,
                headers=headers,
                params=params,
                json=json,
                **kwargs,
            )

            if not request.ok:
                if cls._debug_mode:
                    logger.error(
                        f"[{request.status}] {method} URI: {cls._base_url + path}, {params=}, {json=};\n{await request.text()}"
                    )
                raise aiohttp.client_exceptions.ClientError(
                    detail=f"Failed to perform {cls._base_url + path} {method} request, {params=}, {json=}; {await request.text()}"
                )

            data = await request.json()

            if cls._debug_mode:
                logger.debug(
                    f"[{request.status}] {method} URI: {cls._base_url + path}, {params=}, {json=}"
                )

            return data

    @classmethod
    async def _http_method(
        cls, path: str, params: dict = None, json: dict = None, **kwargs
    ):
        return await cls._request(
            method=sys._getframe().f_back.f_code.co_name.upper()[1:],
            path=path,
            params=params,
            json=json,
            **kwargs,
        )

    @classmethod
    async def _get(cls, path: str, params: dict = None, json: dict = None, **kwargs):
        return await cls._http_method(path=path, params=params, json=json, **kwargs)

    @classmethod
    async def _post(cls, path: str, params: dict = None, json: dict = None, **kwargs):
        return await cls._http_method(path=path, params=params, json=json, **kwargs)

    @classmethod
    async def _put(cls, path: str, params: dict = None, json: dict = None, **kwargs):
        return await cls._http_method(path=path, params=params, json=json, **kwargs)

    @classmethod
    async def _patch(cls, path: str, params: dict = None, json: dict = None, **kwargs):
        return await cls._http_method(path=path, params=params, json=json, **kwargs)

    @classmethod
    async def _delete(cls, path: str, params: dict = None, json: dict = None, **kwargs):
        return await cls._http_method(path=path, params=params, json=json, **kwargs)
