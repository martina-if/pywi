# -*- coding: utf-8 -*-
import web
import htmlize
import os

# TODO:
# - Crear clase page o node, en vez de diccionarios. Factible usar
#	objetos con templates fácilmente?
# - os.path.join
# - Meter funciones en clases
# - Poner la mayor parte del html en templates

DATA_DIR = "data/"
EXTENSION = "txt"

urls = (
		'/',                'index',
		'/favicon.ico',		'favicon',
		'/icons/(.*)',    	'static',
		'/static/(.*)',   	'static',
		'/(.*)',          	'node',
		)

def delete_extension(filename):
	return os.path.splitext(filename)[0]

class favicon:
	def GET(self):
		return open(str("static/favicon.ico"), 'r').read()

def is_page(filename, extension = EXTENSION):
	try:
		ext = filename.split('.')[-1]
		return ext == extension
	except ValueError:
		return False


def get_menu(path):
	# De momento sólo muestro un nivel de CATEGORÍAS
	data_dirs = [{'title': os.path.basename(d), 'path': d} 
				for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	return data_dirs


t_globals = {
		'htmlize': htmlize.htmlize,
}


render = web.template.render('templates/', globals=t_globals)

class index:
    def GET(self):
		# Esto es para coger el nombre del QS
		#i = web.input(name=None)
		#return render.index(i.name)
		# Esto coge el nombre de la URL
		return render.index()

class node:
	def GET(self, page_url):
		self.current_page = {}
		self.current_page['url'] = str(page_url)
		self.current_page['title'] = os.path.basename(str(page_url))
		self.current_page['path'] = os.path.join(DATA_DIR, self.current_page['url'])
		if os.path.isdir(self.current_page['path']):
		#try:
			self.current_dir = self.current_page['path']
			print "CURRENT: ", self.current_page
			return render.dir(self.current_page['path'], self)
		else:
			self.current_dir = os.path.dirname(self.current_page['path'])
			self.current_page['path'] = os.path.join(self.current_page['path'] + 
					"." + EXTENSION)
			print "CURRENT: ", self.current_page
			return render.page(self.current_page['path'], self)
		#except:
			#return render.notfound()


	def get_menu_page(self):
		# De momento sólo muestro un nivel de CATEGORÍAS
		data_dirs = [
					{'title': os.path.basename(d), 
					#'url': os.path.join(os.path.dirname(self.current_page['url']), d),
					'url': d,
					'path': os.path.join(self.current_dir,d)} 
					for d in os.listdir(self.current_dir)
					if os.path.isdir(os.path.join(self.current_dir, d))
					]
		return render.menu(data_dirs)

	def get_menu_dir(self):
		# De momento sólo muestro un nivel de CATEGORÍAS
		data_dirs = [
					{'title': os.path.basename(d), 
					'url': os.path.join("/", self.current_page['url'], d),
					'path': os.path.join(self.current_dir,d)} 
					for d in os.listdir(self.current_dir)
					if os.path.isdir(os.path.join(self.current_dir, d))
					]
		return render.menu(data_dirs)

	def get_pages_from_folder(self):
		data_pages = [
					{'title': delete_extension(f), 
					'path': os.path.join(self.current_dir,f),
					'url': delete_extension(os.path.join("/", self.current_page['url'], f)),
					} for f in os.listdir(self.current_dir) 
			if is_page(os.path.join(self.current_dir, f))]
		return data_pages


class static:
	def GET(self, filename=None):
		print("KAKOTA==================== ")
		print self
		return open(str(filename), 'r').read()

if __name__ == "__main__": 
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()


