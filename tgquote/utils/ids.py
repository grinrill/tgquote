def getSenderId(message):
  if chat := message.get('sender_chat'):
    return chat['id']
  return message['from']['id']

__all__ = [
  'getSenderId',
]