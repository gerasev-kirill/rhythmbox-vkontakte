import gconf

class VkontakteConfig(object):
	def __init__(self):
		self.gconf_keys = {
			'filemask': {"path":'/apps/rhythmbox/plugins/vkontakte/filemask',"type":str,
					"default":"~/Music/%A - %T.mp3"},
			'temporary_token':{"path":'/apps/rhythmbox/plugins/vkontakte/temporary_token',"type":str,
					"default":""},
			'search_only_in_my_audio':{"path":'/apps/rhythmbox/plugins/vkontakte/search_only_in_my_audio',"type":bool,
					"default":False},
			'sort_type':{"path":'/apps/rhythmbox/plugins/vkontakte/sort_type',"type":int,
					"default":2},
			'future':{'path':'/apps/rhythmbox/plugins/vkontakte/future',"type":str,
					"default":""}
		}

		self.gconf = gconf.client_get_default()
		for key in self.gconf_keys.keys():
			if not self.get(key):
				self.set(key,self.gconf_keys[key]["default"]) 
		

	def get(self, key):
		if self.gconf_keys[key]["type"]==str:
			return self.gconf.get_string(self.gconf_keys[key]["path"])
		elif self.gconf_keys[key]["type"]==bool:
			return self.gconf.get_bool(self.gconf_keys[key]["path"])
		elif self.gconf_keys[key]["type"]==int:
			return self.gconf.get_int(self.gconf_keys[key]["path"])
		

	def set(self, key, value):
		if self.gconf_keys[key]["type"]==str:
			self.gconf.set_string(self.gconf_keys[key]["path"], value)
		elif self.gconf_keys[key]["type"]==bool:
			return self.gconf.set_bool(self.gconf_keys[key]["path"], value)
		elif self.gconf_keys[key]["type"]==int:
			return self.gconf.set_int(self.gconf_keys[key]["path"], value)
