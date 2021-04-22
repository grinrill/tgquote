from jinja2 import Environment, FileSystemLoader
from jinja2 import Environment, FileSystemLoader
from .filegetters import BaseFileGetter
from . import utils
import typing

env = Environment(
    loader=FileSystemLoader('./templates'),
    enable_async=True,
)


async def messages_to_html(
    messages: typing.List[dict],
    env: Environment = env,
    **kwargs
  ):
  template = env.get_template('index.jinja2')

  html = await template.render_async(
    messages = messages,
    utils = utils,
    **kwargs
  )
  return html