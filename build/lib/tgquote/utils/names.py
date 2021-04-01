def getFullName(user: dict):
  if not 'id' in user:
    message = user
    user = message.get('from') or message.get('sender_chat')
  if title := user.get('title'):
    return title
  if user.get('last_name'):
    return '%s %s'%(user['first_name'], user['last_name'])
  return user['first_name']

def getForwardSenderName(message: dict):
  if chat := message.get('forward_from'):
    return getFullName(chat)
  if chat := message.get('forward_from_chat'):
    sender_name = getFullName(chat)
    if forward_signature := message.get('forward_signature'):
      sender_name += f' ({forward_signature})'
    return sender_name
  if forward_sender_name := message.get('forward_sender_name'):
    return forward_sender_name

def getViaBot(message):
  if via_bot := message.get('via_bot'):
    return 'via @%s'%via_bot['username']
  return ''

__all__ = [
  'getFullName',
  'getForwardSenderName',
  'getViaBot',
]