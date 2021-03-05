from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader('./templates'),
    # enable_async=True,
    # autoescape=select_autoescape(['html', 'xml', 'jinja2'])
)
template = env.get_template('messages')


def message2html(
  messages: typing.Union[
    dict,
    typing.List[dict]]
  ):
