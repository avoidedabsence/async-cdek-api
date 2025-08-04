__version__ = "0.1.5"
__author__ = "Alexey P."
__email__ = "i@apechenin.ru"

from .client.cdek import CDEKAPIClient
from .client.common import APIClient

__all__ = [
    "CDEKAPIClient",
    "APIClient",
]

