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
		self.set_title("Vkontakte Rhythmbox")
		vbox=gtk.VBox()
		self.progressBar=gtk.ProgressBar()
		browser=webkit.WebView()
		scrolledWindow=gtk.ScrolledWindow()
		scrolledWindow.add(browser)
		label=gtk.Label()
		label.set_markup("<big><b>You neet to auth at vk.com!</b></big>")
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
	def __init__(self, search_term, db, entry_type,config):
		self.search_term = search_term
		self.db = db
		self.entry_type = entry_type
		self.query_model = rhythmdb.QueryModel()
		self.search_complete = False
		self.entries_hashes = []
		self.track_number=0
		self.config=config
		
	def is_complete(self):
		return self.search_complete
	
	def is_in_result(self,result):
		if self.search_term in result.title.lower() :
			return True
		elif self.search_term in result.artist.lower() :
			return True
		return False

	def add_entry(self, result):
		entry = self.db.entry_lookup_by_location(result.url)

		if self.config.get("search_only_in_my_audio"):
			if not self.is_in_result(result):
				return
		simple_title=result.title.lower().replace(" ","").replace("-","").replace(".","").replace(",","").replace("!","").replace("'","")
		if simple_title in self.entries_hashes:
			return
		self.entries_hashes.append(simple_title)
		if entry is None:
			entry = self.db.entry_new(self.entry_type, result.url)
			if result.title:
				self.db.set(entry, rhythmdb.PROP_TITLE, result.title)
			if result.duration:
				self.db.set(entry, rhythmdb.PROP_DURATION, result.duration)
			if result.artist:
				self.db.set(entry, rhythmdb.PROP_ARTIST, result.artist)
		self.track_number+=1
		self.db.set(entry, rhythmdb.PROP_TRACK_NUMBER, self.track_number)
					
		self.query_model.add_entry(entry, -1)

	def on_token_recieved(self, token):
		self.config.set("temporary_token",token)
		self.start()

	def on_search_results_recieved(self, data):
		diction=eval(data)
		if diction.has_key("error"):
			auth=VkontakteAuth(self.on_token_recieved)
			return
		diction=diction["response"]
		diction=diction[1:]
		self.track_number=0
		for audio in diction:
			self.add_entry(VkontakteResult(audio,self.config))
		self.search_complete = True

	# Starts searching
	def start(self):
		if self.config.get("use_permanent_token"):
			token = self.config.get("permanent_token")
		else:
			token = self.config.get("temporary_token")

		if self.config.get("search_only_in_my_audio"):
			path="https://api.vk.com/method/audio.get?count=400&access_token=%s" % token
		else:
			auto_complete=self.config.get("auto_complete")
			if auto_complete:
				auto_complete="&auto_complete=1"
			else:
				auto_complete=""
			path="https://api.vk.com/method/audio.search?q=%s%s&count=400&sort=%s&access_token=%s" % (urllib2.quote(self.search_term), auto_complete ,self.config.get("sort_type"),token )
		loader = rb.Loader()
		loader.get_url(path, self.on_search_results_recieved)



class VkontakteMyLibrary:
	def __init__(self, db, entry_type,config):
		self.db = db
		self.entry_type = entry_type
		self.query_model = rhythmdb.QueryModel()
		self.search_complete = False
		self.config=config
		
	def is_complete(self):
		return self.search_complete

	def add_entry(self, result):
		entry = self.db.entry_lookup_by_location(result.url)
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
		self.config.set("temporary_token",token)
		self.start()

	def on_search_results_recieved(self, data):
		diction=eval(data)
		if diction.has_key("error"):
			auth=VkontakteAuth(self.on_token_recieved)
			return
		diction=diction["response"]
		diction=diction[1:]
		for audio in diction:
			self.add_entry(VkontakteResult(audio,self.config))
		self.search_complete = True

	# Starts searching
	def start(self):
		if self.config.get("use_permanent_token"):
			token = self.config.get("permanent_token")
		else:
			token = self.config.get("temporary_token")

		path="https://api.vk.com/method/audio.get?count=400&access_token=%s" % token
		loader = rb.Loader()
		loader.get_url(path, self.on_search_results_recieved)

