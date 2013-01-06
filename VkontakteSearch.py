# - encoding: utf8 - 
#
# Copyright © 2010 Alexey Grunichev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import rhythmdb,webkit,gtk
from VkontakteResult import VkontakteResult
from VkontakteConfig import VkontakteConfig
import urllib2
import rb

APP_ID = 1850196

class VkontakteAuth(gtk.Window):
	def __init__(self, callback_function):
		super(VkontakteAuth, self).__init__()
		self.callback_function=callback_function
		self.set_title("Vk Auth")
		vbox=gtk.VBox()
		self.progressBar=gtk.ProgressBar()
		browser=webkit.WebView()
		scrolledWindow=gtk.ScrolledWindow()
		scrolledWindow.add(browser)
		label=gtk.Label("You neet to auth at vk.com!")
		vbox.pack_start(label,False)
		vbox.pack_start(scrolledWindow,True)
		vbox.pack_start(self.progressBar,False)
		browser.connect("load-finished",self.load_finished)
		browser.connect("load-progress-changed",self.progress)
		browser.load_uri("https://oauth.vk.com/authorize?client_id=%s&scope=audio&redirect_uri=http://oauth.vk.com/blank.html&display=page&response_type=token" % APP_ID)
		self.add(vbox)
		self.show_all()
		self.resize(600,400)
		gtk.main()

	def load_finished(self,w,frame):
		i=frame.get_uri().find("access_token=")
		if i>0:
			uri=frame.get_uri()
			self.destroy()
			i=i+"access_token=".__len__()
			j=uri.find("&",i)
			token=uri[i:j]
			self.callback_function(token)
			
		
	def progress(self,web,amount):
		self.progressBar.set_fraction(amount/100.0)

 
class VkontakteSearch:
	def __init__(self, search_term, db, entry_type):
		self.search_term = search_term
		self.db = db
		self.entry_type = entry_type
		self.query_model = rhythmdb.QueryModel()
		self.search_complete = False
		self.entries_hashes = []
		self.preferences=VkontakteConfig()
		
	def is_complete(self):
		return self.search_complete
	
	def add_entry(self, result):
		entry = self.db.entry_lookup_by_location(result.url)
		# add only distinct songs (unique by title+artist+duration) to prevent duplicates
		if result.title.lower() in self.entries_hashes:
			return
		self.entries_hashes.append(result.title.lower())
		if entry is None:
			entry = self.db.entry_new(self.entry_type, result.url)
			if result.title:
				self.db.set(entry, rhythmdb.PROP_TITLE, result.title)
			if result.duration:
				self.db.set(entry, rhythmdb.PROP_DURATION, result.duration)
			if result.artist:
				self.db.set(entry, rhythmdb.PROP_ARTIST, result.artist)
		self.query_model.add_entry(entry, -1)

	def on_token_recieved(self, token):
		self.preferences.set("temporary_token",token)
		self.start()

	def on_search_results_recieved(self, data):
		diction=eval(data)
		if diction.has_key("error"):
			auth=VkontakteAuth(self.on_token_recieved)
			return
		diction=diction["response"]
		diction=diction[1:]
		for audio in diction:
			self.add_entry(VkontakteResult(audio))
		self.search_complete = True

	# Starts searching
	def start(self):
		path="https://api.vk.com/method/audio.search?q=%s&count=300&access_token=%s" % (urllib2.quote(self.search_term), self.preferences.get("temporary_token") )
		loader = rb.Loader()
		loader.get_url(path, self.on_search_results_recieved)

