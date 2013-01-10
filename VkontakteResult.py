# - encoding: utf8 - 
#
# Copyright © 2010 Alexey Grunichev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class VkontakteResult:
	def __init__(self, entry,config):
		# Store the function. This will be called when we are ready to be added to the db.
		self.title = entry['title']
		self.duration = entry['duration']
		self.artist = entry['artist']
		self.url = entry['url'].replace("\\","")

		self.title=self.remove_crap(self.title,config)
		if config.get("use_on_artist"):
			self.artist=self.remove_crap(self.artist,config)
			
	

	def remove_crap(self,w,config):
		if w.startswith(" "):
			w=w[1:]
		try:
			if w[-1]==" ":
				w=w[:-1]
		except:
			pass
		if config.get("rm_spaces"):
			w=w.replace("  "," ")
		if config.get("rm_exp"):
			try:
				expressions="["+config.get("expressions")+"]"
				expressions=eval(expressions)
				for exp in expressions:
					i=w.find(exp)
					if i>1:
						w=w[:i]
			except:
				pass
		w=w.replace("`","'")
		w=w.replace("' ","'")
		w=w.replace("*","'")
		w=w.replace("`","'")
		w=w.replace("\n"," ")
		return w
		
		
