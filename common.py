import re
import sys
from contextlib import asynccontextmanager
from typing import Literal

import aiohttp.client_exceptions
from aiohttp import ClientSession


class APIClient:
	_base_url: str = None
	_client_name: str = __qualname__

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
				raise aiohttp.client_exceptions.ClientError(
					detail=f"Failed to perform {cls._base_url + path} {method} request, {params=}, {json=}; {await request.text()}"
				)

			data = await request.json()

			return data

	@classmethod
	async def _http_method(
		cls, path: str, params: dict = None, json: dict = None, **kwargs
	):
		return await cls._request(
			method=sys._getframe().f_back.f_code.co_name.upper(),
			path=path,
			params=params,
			json=json,
			**kwargs,
		)

	@classmethod
	async def get(cls, path: str, params: dict = None, json: dict = None, **kwargs):
		return await cls._http_method(path=path, params=params, json=json, **kwargs)

	@classmethod
	async def post(cls, path: str, params: dict = None, json: dict = None, **kwargs):
		return await cls._http_method(path=path, params=params, json=json, **kwargs)

	@classmethod
	async def put(cls, path: str, params: dict = None, json: dict = None, **kwargs):
		return await cls._http_method(path=path, params=params, json=json, **kwargs)

	@classmethod
	async def patch(cls, path: str, params: dict = None, json: dict = None, **kwargs):
		return await cls._http_method(path=path, params=params, json=json, **kwargs)

	@classmethod
	async def delete(cls, path: str, params: dict = None, json: dict = None, **kwargs):
		return await cls._http_method(path=path, params=params, json=json, **kwargs)
