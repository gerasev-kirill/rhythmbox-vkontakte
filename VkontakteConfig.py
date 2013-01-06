import gconf

class VkontakteConfig(object):
	def __init__(self):
		self.gconf_keys = {
			'filemask': '/apps/rhythmbox/plugins/vkontakte/filemask',
			'temporary_token':'/apps/rhythmbox/plugins/vkontakte/temporary_token'
		}

		self.gconf = gconf.client_get_default()
		if not self.get('filemask'):
			self.set("filemask", "~/Music/%A - %T.mp3")
		if not self.get('temporary_token'):
			self.set("temporary_token", "")
		

	def get(self, key):
		if self.gconf.get_string(self.gconf_keys[key]):
			return self.gconf.get_string(self.gconf_keys[key])
		else:
			return ""

	def set(self, key, value):
		self.gconf.set_string(self.gconf_keys[key], value)
