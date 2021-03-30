templates_list = dict(
  photo = 'photo_message.jinja2',
  document = 'document_message.jinja2',
  voice = 'voice_message.jinja2',
  video_note = 'video_note_message.jinja2',
  sticker = 'sticker_message.jinja2',
  animation = 'animation_message.jinja2',
  _ = 'base_message.jinja2',
)

def get_template(message, templates=templates_list):
	for key in message.keys():
		if template := templates.get(key):
			return template
	return templates.get('_')

__all__ = [
	'get_template',
	'templates_list'
]