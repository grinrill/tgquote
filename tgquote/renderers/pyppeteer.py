from .base import BaseRenderer
import asyncio
import io
import tempfile
import typing
import pathlib

try:
  from pyppeteer import launch
except ModuleNotFoundError:
  pass

class PyppeteerRenderer(BaseRenderer):
  def __init__(
    self,
    screenshot_params = {
      'type': 'png',
      'omitBackground': True,
    },
    file_format: str = 'png',
    browser = None,
    **launcher_options
  ):
    # if pyppeteer not instaled it will raise ModuleNotFoundError
    import pyppeteer

    if file_format:
      screenshot_params['type'] = file_format
    self.screenshot_params = screenshot_params
    self.launcher_options = launcher_options
    self.browser = browser
    
  async def render(
    self, 
    html: str, 
    css: str, 
    file_format: str,
    file: typing.Union[str, io.BytesIO] = None,
    screenshot_params = {},
  ):
    if not self.browser:
      self.browser = await launch(self.launcher_options)
    
    if file is None:
      file = io.BytesIO()
    elif isinstance(file, (str, pathlib.PosixPath)):
      file = open(file, 'w+b')

    file_format = file_format or self.file_format
    screenshot_params = {**self.screenshot_params, **screenshot_params}
    screenshot_params['type'] = file_format

    content = f'<style>{css}</style> {html}'

    page = await self.browser.newPage()
    await page.setContent(content)
    await page.waitForSelector('.messages')
    messages = await page.querySelector('.messages')
    
    with tempfile.NamedTemporaryFile() as f:
      screenshot_params.setdefault('path', f.name)
      await messages.screenshot(screenshot_params)
      
      file.write(f.read())
      file.seek(0)
      return file

  async def close(self):
    try:
      await self.browser.close()
    except:
      pass