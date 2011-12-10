# -*- coding: utf-8 -*-
import web
import htmlize
import os

# TODO:
# - os.path.join

#DATA_DIR = "/home/marta/software/sources/pywi/data/"
DATA_DIR = "data/"
EXTENSION = "txt"

urls = (
		'/',                'index',
		'/favicon.ico',		'favicon',
		'/icons/(.*)',    	'static',
		'/static/(.*)',   	'static',
		'/(.*)',          	'page',
		)

class favicon:
	def GET(self):
		return open(str("static/favicon.ico"), 'r').read()

def is_page(filename, extension = EXTENSION):
	try:
		basename, ext = filename.split('.')
		return ext == extension
	except ValueError:
		return False


#TODO TODO TODO 
def get_menu(path):
	#def get_submenu(path):
		#data_dirs =  [d for d in os.listdir(path) 
				#if os.path.isdir(os.path.join(path, d))]
		#data_pages = [f for f in os.listdir(path) 
				#if is_page(os.path.join(path, f))]
		#pages = []
		#for p in data_pages:
			#pages = pages + [{'title':p, 'path':os.path.join(path,p)}]

		#for i in data_dirs:
			#pages = pages + [get_submenu(os.path.join(path,i))]
		#return pages
		
	#data_pages = get_submenu(self.current_dir)
	###########################################
	# De momento sólo muestro un nivel de CATEGORÍAS
	data_dirs = [{'title': os.path.basename(d), 'path': d} 
				for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	return data_dirs

def get_menu_html(path):
	path = os.path.dirname(path)
	def render_item(item):
		if type(item) is list:
			try:
				html = "<ul>\n" + render_item(item[0]) + "</ul>\n" + render_item(item[1:])
			except IndexError:
				html = "<ul>\n" + render_item(item[0]) + "</ul>\n"
			return html
		elif type(item) is dict:
			return ("\t<li> <a href=\"" + item['path'] + "\"> "+ 
				item['title'] + "</a></li>\n")
		else: # No debería ocurrir
			return ''
	menu = get_menu(path)
	print menu
	html = '<div id=menu>\n' + render_item(menu) + "</div>"
	return html

	

t_globals = {
		'htmlize': htmlize.htmlize,
		'get_menu_html': get_menu_html,
}

render = web.template.render('templates/', globals=t_globals)

class index:
    def GET(self):
		# Esto es para coger el nombre del QS
		#i = web.input(name=None)
		#return render.index(i.name)
		# Esco coge el nombre de la URL
		return render.index()

class page:
	def GET(self, page):
		#try:
		if os.path.isdir(os.path.join(DATA_DIR, str(page))):
			return "DIRECTORIO " + str(page)
		else:
			page_path = os.path.join(DATA_DIR, str(page) + "." + EXTENSION)
			self.current_dir = os.path.dirname(page_path)
			self.current_page = page_path
			return render.page(page_path)
		#except:
			#return render.notfound()

class static:
	def GET(self, filename=None):
		print("KAKOTA==================== ")
		print self
		return open(str(filename), 'r').read()

if __name__ == "__main__": 
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()


