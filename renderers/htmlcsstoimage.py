from .base import BaseRenderer
import aiohttp
import io
import typing

class HtmlCssToImageRenderer(BaseRenderer):
  api_url: str
  api_id: str
  api_key: str

  def __init__(
    self, 
    api_id: str,
    api_key: str,
    file_format: str = 'png',
    api_url: str='https://hcti.io/v1/image',
    **api_params
  ):
    self.api_url = api_url
    self.api_id = api_id
    self.api_key = api_key
    self.file_format = file_format
    self.api_params = api_params
    self.session = None

  async def render(
    self, 
    html: str, 
    css: str, 
    file_format: str,
    file: typing.Union[str, io.BytesIO] = None,
    api_url = None,
    api_id = None,
    api_key = None,
    **api_params,
  ):
    if not self.session:
      self.session = await aiohttp.ClientSession()

    api_url = api_url or self.api_url
    api_id = api_id or self.api_id
    api_key = api_key or self.api_key
    file_format = file_format or self.file_format
    api_params = {**self.api_params, **api_params}

    if file is None:
      file = io.BytesIO()
    elif isinstance(file, (str, pathlib.PosixPath)):
      file = open(file, 'w+b')

    data = {
      'html': html,
      'css': css,
      **api_params,
    }
    auth = aiohttp.BasicAuth(api_id, api_key)

    if file_format not in ['jpg', 'png', 'webp']:
      raise ValueError(f'file_format must be jpg, png or webp, not {file_format}')

    resp = await self.session.post(
      api_url,
      data=data,
      auth=auth, 
    )
    result = await resp.json()

    image_resp = await self.session.get(result['url']+'.'+file_format)

    file.write(await image_resp.read())
    file.seek(0)

    return file

  async def close(self):
    try:
      await seld.session.close()
    except:
      pass