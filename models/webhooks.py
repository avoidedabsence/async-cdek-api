from pydantic import BaseModel, Field
from ..enums import WebhookType


class WebhookRequest(BaseModel):
	url: str = Field(..., description="Webhook URL")
	type: WebhookType = Field(WebhookType.ORDER_STATUS, description="Webhook type")


class WebhookResponse(BaseModel):
	uuid: str = Field(..., description="Webhook UUID")
	url: str = Field(..., description="Webhook URL")
	type: WebhookType = Field(..., description="Webhook type")
	account: str | None = Field(None, description="Account identifier")


class WebhookInfo(BaseModel):
	uuid: str = Field(..., description="Webhook UUID")
	url: str = Field(..., description="Webhook URL")
	type: WebhookType = Field(..., description="Webhook type")
	account: str | None = Field(None, description="Account identifier")
	created_datetime: str | None = Field(None, description="Creation datetime")
	is_active: bool | None = Field(None, description="Is webhook active")
