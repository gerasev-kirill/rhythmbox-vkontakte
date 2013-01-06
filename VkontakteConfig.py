import gconf

class VkontakteConfig(object):
	def __init__(self):
		self.gconf_keys = {
			'filemask': {"path":'/apps/rhythmbox/plugins/vkontakte/filemask',"type":str},
			'temporary_token':{"path":'/apps/rhythmbox/plugins/vkontakte/temporary_token',"type":str},
			'search_only_in_my_audio':{"path":'/apps/rhythmbox/plugins/vkontakte/search_only_in_my_audio',"type":bool}
		}

		self.gconf = gconf.client_get_default()
		if not self.get('filemask'):
			self.set("filemask", "~/Music/%A - %T.mp3")
		if not self.get('temporary_token'):
			self.set("temporary_token", "")
		if not self.get('search_only_in_my_audio'):
			self.set("search_only_in_my_audio", False)
		

	def get(self, key):
		if self.gconf_keys[key]["type"]==str:
			return self.gconf.get_string(self.gconf_keys[key]["path"])
		elif self.gconf_keys[key]["type"]==bool:
			return self.gconf.get_bool(self.gconf_keys[key]["path"])
		

	def set(self, key, value):
		if self.gconf_keys[key]["type"]==str:
			self.gconf.set_string(self.gconf_keys[key]["path"], value)
		elif self.gconf_keys[key]["type"]==bool:
			return self.gconf.set_bool(self.gconf_keys[key]["path"], value)
