from .preprocessing import preprocessMessagesToDict
from .renderers import BaseRenderer
from .filegetters import BaseFileGetter
from .message2html import messagesToHtml

from jinja2 import Environment, ChoiceLoader, BaseLoader, FileSystemLoader
import typing
import io

from pathlib import Path
module = Path(__file__).parent

class TelegramImageRenderer:
  def __init__(
    self,
    renderer: BaseRenderer,
    filegetter: BaseFileGetter,
    file_format: str = 'png',
    styles: typing.Union[str, io.BytesIO, io.StringIO] = str(module/'css/light.css'),
    append_styles: typing.Union[str, io.BytesIO, io.StringIO] = None,
    jinja2_loader: BaseLoader = None,
    jinja2_env: Environment = None,
  ):
    self.renderer = renderer
    self.filegetter = filegetter  
    self.file_format = file_format

    if jinja2_env:
      self.env = jinja2_env
    else:
      if jinja2_loader:
        loader = ChoiceLoader([
          jinja2_loader,
          FileSystemLoader(module/'templates')
        ])
      else:
        loader = FileSystemLoader(module/'templates')
      self.env = Environment(
          loader=loader,
          enable_async=True,
      )
    
    if isinstance(styles, str):
      if styles.endswith('.css'):
        self.css = open(styles, 'r+').read()
      else:
        self.css = styles
    else:
      self.css = styles.read()
      if isinstance(self.css, bytes):
        self.css = self.css.decode()
    if append_styles:
      if isinstance(styles, str):
        if append_styles.endswith('.css'):
          append_css = open(append_styles, 'r+').read()
        else:
          append_css = append_styles
      else:
        append_css = append_styles.read()
        if isinstance(append_css, bytes):
          append_css = append_css.decode()
      self.css += append_css
        
  async def render(
    self,
    messages,
    renderer: BaseRenderer = None,
    filegetter: BaseFileGetter = None,
    file_format: str = None,
    styles: typing.Union[str, io.BytesIO, io.StringIO] = None,
    append_styles: typing.Union[str, io.BytesIO, io.StringIO] = None,
    jinja2_loader: BaseLoader = None,
    jinja2_env: Environment = None,
  ):
    renderer = renderer or self.renderer
    filegetter = filegetter or self.filegetter
    file_format = file_format or self.file_format

    env = self.env
    if jinja2_env:
      env = jinja2_env
    else:
      if jinja2_loader:
        loader = ChoiceLoader([
          jinja2_loader,
          FileSystemLoader(module/'templates')
        ])
        env = Environment(
            loader=loader,
            enable_async=True,
        )
    
    if styles:
      if isinstance(styles, str):
        if styles.endswith('.css'):
          css = open(styles, 'r+').read()
        else:
          css = styles
      else:
        css = styles.read()
        if isinstance(self.css, bytes):
          css = css.decode()
    else:
      css = self.css
    if append_styles:
      if isinstance(styles, str):
        if append_styles.endswith('.css'):
          append_css = open(append_styles, 'r+').read()
        else:
          append_css = append_styles
      else:
        append_css = append_styles.read()
        if isinstance(append_css, bytes):
          append_css = append_css.decode()
      css += append_css

    messages = preprocessMessagesToDict(messages)
    html = await messagesToHtml(messages, filegetter, env)
    image = await renderer.render(html, css, file_format)

    return image
