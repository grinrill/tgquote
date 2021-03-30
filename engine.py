from .preprocessing import preprocessMessagesToDict
from .renderers import BaseRenderer
from .filegetters import BaseFileGetter
from .message2html import messagesToHtml
from .utils import templates_list

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
  ):
    self.renderer = renderer
    self.filegetter = filegetter  
    self.templates = templates
    self.file_format = file_format

    # if jinja2_env:
    #   self.env = jinja2_env
    # else:
    #   if jinja2_loader:
    #     loader = ChoiceLoader([
    #       jinja2_loader,
    #       FileSystemLoader(module/'templates')
    #     ])
    #   else:
    #     loader = FileSystemLoader(module/'templates')
    #   self.env = Environment(
    #       loader=loader,
    #       enable_async=True,
    #   )
    
    # if isinstance(css, str):
    #   if css.endswith('.css'):
    #     self.css = open(css, 'r+').read()
    #   else:
    #     self.css = css
    # else:
    #   self.css = css.read()
    #   if isinstance(self.css, bytes):
    #     self.css = self.css.decode()
    # if append_css:
    #   if isinstance(css, str):
    #     if append_css.endswith('.css'):
    #       append_css = open(append_css, 'r+').read()
    #     else:
    #       append_css = append_css
    #   else:
    #     append_css = append_css.read()
    #     if isinstance(append_css, bytes):
    #       append_css = append_css.decode()
    #   self.css += append_css

    self.env = self.get_env(jinja2_loader, jinja2_env)
    self.css = self.get_css(css, append_css)

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
  ):
    renderer = renderer or self.renderer
    filegetter = filegetter or self.filegetter
    templates = templates or self.templates
    file_format = file_format or self.file_format

    # env = self.env
    # if jinja2_env:
    #   env = jinja2_env
    # else:
    #   if jinja2_loader:
    #     loader = ChoiceLoader([
    #       jinja2_loader,
    #       FileSystemLoader(module/'templates')
    #     ])
    #     env = Environment(
    #         loader=loader,
    #         enable_async=True,
    #     )
    
    # if css:
    #   if isinstance(css, str):
    #     if css.endswith('.css'):
    #       css = open(css, 'r+').read()
    #     else:
    #       css = css
    #   else:
    #     css = css.read()
    #     if isinstance(self.css, bytes):
    #       css = css.decode()
    # else:
    #   css = self.css
    # if append_css:
    #   if isinstance(css, str):
    #     if append_css.endswith('.css'):
    #       append_css = open(append_css, 'r+').read()
    #     else:
    #       append_css = append_css
    #   else:
    #     append_css = append_css.read()
    #     if isinstance(append_css, bytes):
    #       append_css = append_css.decode()
    #   css += append_css

    env = self.get_env(jinja2_loader, jinja2_env)
    css = self.get_css(css, append_css)

    messages = preprocessMessagesToDict(messages)
    html = await messagesToHtml(messages, env, files=filegetter, templates=templates)
    image = await renderer.render(html, css, file_format)

    return image

  async def close(self):
    await self.renderer.close()
