import gtk

class VkontakteConfigDialog (object):
	def __init__(self, builder_file, config):
		self.config = config

		self.builder = gtk.Builder()
		self.builder.add_from_file(builder_file)

		self.dialog = self.builder.get_object('dialog')
		keys_checkbox=config.get_keys_by_type(bool)
		self.set_checkbox(keys_checkbox)
		keys_entry=config.get_keys_by_type(str)
		self.set_entry(keys_entry)
#		self.filemask = builder.get_object("filemask")
#		self.filemask.set_text(self.config.get('filemask'))

#		self.dialog.connect("response", self.dialog_response)

	def set_entry(self,keys):
		for key in keys:
			try:
				entry=self.builder.get_object(key.replace("_","-")+"-e")
				entry.set_text(self.config.get(key))
			except:
				fc=self.builder.get_object(key.replace("_","-")+"-fc")
				fc.set_filename(self.config.get(key))
		
	def set_checkbox(self,keys):
		for key in keys:
			try:
				checkbox=self.builder.get_object(key.replace("_","-")+"-c")
				checkbox.set_active(self.config.get(key))
			except:
				radiobox=self.builder.get_object(key.replace("_","-")+"-r")
				radiobox.set_active(self.config.get(key))

	def get_dialog (self):
		return self.dialog

	def dialog_response (self, dialog, response):
#		self.config.set('filemask', self.filemask.get_text())
		dialog.hide()
