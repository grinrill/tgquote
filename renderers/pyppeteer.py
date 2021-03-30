from .base import BaseRenderer
import asyncio
import io
import tempfile

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
    screenshot_params = {},
  ):
    if not self.browser:
      self.browser = await launch(self.launcher_options)

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
      
      f2 = io.BytesIO()
      f2.write(f.read())
      f2.seek(0)
      return f2

  async def close(self):
    try:
      await self.browser.close()
    except:
      pass