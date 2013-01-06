# - encoding: utf8 - 
#
# Copyright © 2010 Alexey Grunichev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#https://api.vk.com/method/audio.search?q=gaga&access_token=bbec11a1f937857295e1cbcd99ee45595fe1ed81b2d975c746bdd0e5a391627b40d99831578a23abd592f

#https://oauth.vk.com/authorize?client_id=1850196&scope=audio&redirect_uri=http://oauth.vk.com/blank.html&display=page&response_type=token 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import rhythmdb
from xml.dom import minidom
from VkontakteResult import VkontakteResult
import urllib2
import hashlib
import rb
from html_decode import decode_htmlentities

APP_ID = 1850196
SECRET_KEY = 'nk0n6I6vjQ'
USER_ID = 76347967

class VkontakteSearch:
	def __init__(self, search_term, db, entry_type):
		self.search_term = search_term
		self.db = db
		self.entry_type = entry_type
		self.query_model = rhythmdb.QueryModel()
		self.search_complete = False
		self.entries_hashes = []
		
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
				self.db.set(entry, rhythmdb.PROP_TITLE, decode_htmlentities(result.title))
			if result.duration:
				self.db.set(entry, rhythmdb.PROP_DURATION, result.duration)
			if result.artist:
				self.db.set(entry, rhythmdb.PROP_ARTIST, decode_htmlentities(result.artist))
		self.query_model.add_entry(entry, -1)

	def on_search_results_recieved(self, data):
		diction=eval(data)
		diction=diction["response"]
		diction=diction[1:]
		for audio in diction:
			self.add_entry(VkontakteResult(audio))
		self.search_complete = True

	# Starts searching
	def start(self):
		path="https://api.vk.com/method/audio.search?q=%s&count=300&access_token=bbec11a1f937857295e1cbcd99ee45595fe1ed81b2d975c746bdd0e5a391627b40d99831578a23abd592f" % urllib2.quote(self.search_term)
		loader = rb.Loader()
		loader.get_url(path, self.on_search_results_recieved)

