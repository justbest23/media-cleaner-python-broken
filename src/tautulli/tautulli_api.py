from typing import Optional, List, Tuple, TypeVar, Generic
from config import Config
import requests
from utils import create_api_error_message, create_param_string
from tautulli_responses import ResponseObj

T = TypeVar('T')

class Response(Generic[T]):
    pass

async def get_obj(command: str, params: Optional[List[Tuple[str, str]]] = None) -> ResponseObj[T]:
    config = Config.global_config().tautulli
    client = requests.Client()

    cmd = f"{command}&{create_param_string(params)}"

    url = f"{config.url}/api/v2?apikey={config.api_key}&cmd={cmd}"

    response = await client.get(url)

    if not (200 <= response.status_code < 300):
        code = response.status_code
        raise Exception(create_api_error_message(code, url, "Tautulli"))

    response_data = response.json()

    return response_data
