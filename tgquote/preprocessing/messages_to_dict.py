import typing

try:
  import aiogram
  from aiogram.types.base import TelegramObject
  from aiogram import Bot
except ModuleNotFoundError:
  TelegramObject = None
  Bot = None

def messages_to_dict(
  messages: typing.Union[
    TelegramObject, 
    dict,
    typing.List[
      typing.Union[
        TelegramObject, 
        dict,
        ]
      ]
    ]
  ) -> typing.List[dict]:
  """
  Юзер в качестве сообщений может передать или словарь, 
  или обьект, наследуемый от TelegramObject
  (то есть обьект сообщения),
  или и то и другое вместе в списке.
  Этот метод приводит всю эту шаурму к typing.List[dict]
  """
  # нам в любом случае надо привести все к списку
  if isinstance(messages, (dict, TelegramObject)):
    messages = [messages]

  # приводим все TelegramObject к dict
  for idx, message in enumerate(messages):
    if isinstance(message, dict): continue
    elif (
        TelegramObject is not None  # если aiogram установлен
                                    # то в начале файла мы импортировали TelegramObject
                                    # и он не None
        and issubclass(type(message), TelegramObject)
      ):
      messages[idx] = message.to_python()
    else:
      raise ValueError(
        'Message must be dict or TelegramObject, '
        'not {}'.format(type(message))
        )
  
  return messages
