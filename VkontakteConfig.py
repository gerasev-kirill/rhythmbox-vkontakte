import gconf

class VkontakteConfig(object):
	def __init__(self):
		self.gconf_keys={}
		future_keys = {
			'future':{'path':'/apps/rhythmbox/plugins/vkontakte/future',"type":str,
					"default":""}
		}
		filter_keys = {
			'rm_spaces':{'path':'/apps/rhythmbox/plugins/vkontakte/filter/rm_spaces',"type":bool,
					"default":True},
			'rm_exp':{'path':'/apps/rhythmbox/plugins/vkontakte/filter/rm_exp',"type":bool,
					"default":True},
			'expressions':{'path':'/apps/rhythmbox/plugins/vkontakte/filter/expressions',"type":str,
					"default":"'..','!','?', '. '"},
			'use_on_artist':{'path':'/apps/rhythmbox/plugins/vkontakte/filter/use_on_artist',"type":bool,
					"default":False},

		}
		save_keys = {
			'allways_ask_path':{'path':'/apps/rhythmbox/plugins/vkontakte/save/allways_ask_path',"type":bool,
					"default":True},
			'save_to_dir':{'path':'/apps/rhythmbox/plugins/vkontakte/save/save_to_dir',"type":str,
					"default":""}
		}
		main_keys = {
			'filemask': {"path":'/apps/rhythmbox/plugins/vkontakte/filemask',"type":str,
					"default":"%A - %T.mp3"},
			'temporary_token':{"path":'/apps/rhythmbox/plugins/vkontakte/temporary_token',"type":str,
					"default":""},
			'permanent_token':{"path":'/apps/rhythmbox/plugins/vkontakte/permanent_token',"type":str,
					"default":""},
			'use_permanent_token':{"path":'/apps/rhythmbox/plugins/vkontakte/use_permanent_token',"type":bool,
					"default":False},
			'search_only_in_my_audio':{"path":'/apps/rhythmbox/plugins/vkontakte/search_only_in_my_audio',"type":bool,
					"default":False},
			'sort_type':{"path":'/apps/rhythmbox/plugins/vkontakte/sort_type',"type":int,
					"default":2},
			'auto_complete':{'path':'/apps/rhythmbox/plugins/vkontakte/auto_complete',"type":bool,
					"default":True}
		}
		self.gconf_keys.update(main_keys)
		self.gconf_keys.update(save_keys)
		self.gconf_keys.update(filter_keys)

		self.gconf = gconf.client_get_default()
		for key in self.gconf_keys.keys():
			if self.gconf.get(self.gconf_keys[key]["path"])==None:
				self.set(key,self.gconf_keys[key]["default"])
		


	def get_keys_by_type(self,key_type):
		keys=[]
		for key in self.gconf_keys.keys():
			if key_type==self.gconf_keys[key]["type"] and key!='temporary_token':
				keys.append(key)
		return keys
		
	
	def get(self, key):
		if self.gconf_keys[key]["type"]==str:
			return self.gconf.get_string(self.gconf_keys[key]["path"])
		elif self.gconf_keys[key]["type"]==bool:
			return self.gconf.get_bool(self.gconf_keys[key]["path"])
		elif self.gconf_keys[key]["type"]==int:
			return self.gconf.get_int(self.gconf_keys[key]["path"])
		return None
		

	def set(self, key, value):
		if self.gconf_keys[key]["type"]==str:
			self.gconf.set_string(self.gconf_keys[key]["path"], value)
		elif self.gconf_keys[key]["type"]==bool:
			return self.gconf.set_bool(self.gconf_keys[key]["path"], value)
		elif self.gconf_keys[key]["type"]==int:
			return self.gconf.set_int(self.gconf_keys[key]["path"], value)
