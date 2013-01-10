import gtk

class VkontakteConfigDialog (object):
	def __init__(self, builder_file, config):
		self.config = config
		self.builder = gtk.Builder()
		self.builder.add_from_file(builder_file)
		self.dialog = self.get('dialog')

		keys_checkbox=config.get_keys_by_type(bool)
		self.set_checkbox(keys_checkbox)
		keys_entry=config.get_keys_by_type(str)
		self.set_entry(keys_entry)

		self.get("allways_ask_path-r").set_group(\
					self.get("save_to_dir-r"))

		if config.get("allways_ask_path"):
			self.get("allways_ask_path-r").set_active(True)
			self.get("save_to_dir-r").set_active(False)
		else:
			self.get("save_to_dir-r").set_active(True)
			self.get("allways_ask_path-r").set_active(False)
			self.get("save_to_dir-fc").set_sensitive(True)

		self.get("expressions-e").set_sensitive(config.get("rm_exp"))
		self.get("permanent_token-e").set_sensitive(config.get("use_permanent_token"))


		save_to_dir_r=self.get("save_to_dir-r")
		save_to_dir_r.connect("clicked", \
				lambda x:self.get("save_to_dir-fc").set_sensitive( self.get("save_to_dir-r").get_active()))
		rm_exp_c=self.get("rm_exp-c")
		rm_exp_c.connect("clicked",\
				lambda x: self.get("expressions-e").set_sensitive( self.get("rm_exp-c").get_active()))
		use_permanent_token=self.get("use_permanent_token-c")
		use_permanent_token.connect("clicked",\
				lambda x: self.get("permanent_token-e").set_sensitive(self.get("use_permanent_token-c").get_active()))

		self.get("ok-b").connect("clicked",self.on_ok_clicked)		
		self.dialog.connect("response", self.dialog_response)


	def get(self,name):
		return self.builder.get_object(name)
		
	def set_entry(self,keys):
		for key in keys:
			try:
				entry=self.get(key+"-e")
				entry.set_text(self.config.get(key))
			except:
				fc=self.get(key+"-fc")
				fc.set_filename(self.config.get(key))
		
	def set_checkbox(self,keys):
		for key in keys:
			try:
				checkbox=self.get(key+"-c")
				checkbox.set_active(self.config.get(key))
			except:
				radiobox=self.get(key+"-r")
				radiobox.set_active(self.config.get(key))

	'''slots'''
	
	def on_ok_clicked(self,b):
		keys_checkbox=self.config.get_keys_by_type(bool)
		for key in keys_checkbox:
			try:
				checkbox=self.get(key+"-c")
				self.config.set(key,checkbox.get_active())
			except:
				radiobox=self.get(key+"-r")
				self.config.set(key,radiobox.get_active())

					
		keys_entry=self.config.get_keys_by_type(str)
		for key in keys_entry:
			try:
				entry=self.get(key+"-e")
				self.config.set(key,entry.get_text())
			except:
				fc=self.get(key+"-fc")
				self.config.set(key,fc.get_filename())

	def get_dialog (self):
		return self.dialog

	def dialog_response (self, dialog, response):
		dialog.hide()
