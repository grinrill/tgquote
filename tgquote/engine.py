from .preprocessing import base_preprocessing
from .renderers import BaseRenderer
from .filegetters import BaseFileGetter
from .messages_to_html import messages_to_html
from .utils import templates_list, js

from jinja2 import Environment, ChoiceLoader, BaseLoader, FileSystemLoader
import typing
import io

from pathlib import Path, PosixPath
module = Path(__file__).parent


class TelegramImageRenderer:
  def get_env(
    self,
    jinja2_loader: BaseLoader = None,
    jinja2_env: Environment = None,
  ):
    env = getattr(self, 'env', None)
    if jinja2_env:
      env = jinja2_env
    else:
      if jinja2_loader:
        loader = ChoiceLoader([
          jinja2_loader,
          FileSystemLoader(module/'templates')
        ])
      else:
        loader = FileSystemLoader(module/'templates')
      env = Environment(
          loader=loader,
          enable_async=True,
      )

    return env

  def get_css(
    self,
    css: typing.Union[str, io.BytesIO, io.StringIO] = module/'css/light.css',
    append_css: typing.Union[str, io.BytesIO, io.StringIO] = None,
  ):
    if css:
      if isinstance(css, PosixPath):
        css = str(css)
      if isinstance(css, str) and css.endswith('.css'):
        css = open(css, 'r+')
      if hasattr(css, 'read'):
        css = css.read()
      if isinstance(css, bytes):
        css = css.decode()
    else:
      css = getattr(self, 'css', None)

    if append_css:
      if isinstance(append_css, PosixPath):
        append_css = str(append_css)
      if isinstance(append_css, str) and append_css.endswith('.css'):
        append_css = open(append_css, 'r+')
      if hasattr(append_css, 'read'):
        append_css = append_css.read()
      if isinstance(append_css, bytes):
        append_css = append_css.decode()
      css += append_css

    return css

  def __init__(
    self,
    renderer: BaseRenderer,
    filegetter: BaseFileGetter,
    file_format: str = 'png',
    css: typing.Union[str, io.BytesIO, io.StringIO] = module/'css/light.css',
    append_css: typing.Union[str, io.BytesIO, io.StringIO] = None,
    jinja2_loader: BaseLoader = None,
    jinja2_env: Environment = None,
    templates = templates_list,
    preprocessing = base_preprocessing,
  ):
    self.renderer = renderer
    self.filegetter = filegetter  
    self.templates = templates
    self.file_format = file_format
    self.preprocessing = preprocessing

    self.env = self.get_env(jinja2_loader, jinja2_env)
    self.css = self.get_css(css, append_css)

  async def render_html(
    self,
    messages,
    filegetter: BaseFileGetter = None,
    css: typing.Union[str, io.BytesIO, io.StringIO] = None,
    append_css: typing.Union[str, io.BytesIO, io.StringIO] = None,
    jinja2_loader: BaseLoader = None,
    jinja2_env: Environment = None,
    templates = None,
    preprocessing = None,
  ):    
    templates = templates or self.templates
    preprocessing = preprocessing or self.preprocessing
    filegetter = filegetter or self.filegetter

    env = self.get_env(jinja2_loader, jinja2_env)
    css = self.get_css(css, append_css)

    for preprocessor in preprocessing:
        messages = preprocessor(messages)

    html = await messages_to_html(messages, env, files=filegetter, templates=templates)
    html = f'{html} <script>{js}</script>'

    return html, css

  async def render(
    self,
    messages,
    renderer: BaseRenderer = None,
    filegetter: BaseFileGetter = None,
    file_format: str = None,
    css: typing.Union[str, io.BytesIO, io.StringIO] = None,
    append_css: typing.Union[str, io.BytesIO, io.StringIO] = None,
    jinja2_loader: BaseLoader = None,
    jinja2_env: Environment = None,
    templates = None,
    preprocessing = None,
    html: str = None,
  ):
    renderer = renderer or self.renderer
    file_format = file_format or self.file_format

    if not html:
      html, css = await self.render_html(
        messages,
        filegetter,
        css,
        append_css,
        jinja2_loader,
        jinja2_env,
        templates,
        preprocessing,
      )
    image = await renderer.render(html, css, file_format)

    return image

  async def close(self):
    await self.renderer.close()
