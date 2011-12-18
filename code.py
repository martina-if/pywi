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
		'/new',				'new',
		'/favicon.ico',		'favicon',
		'/icons/(.*)',    	'static',
		'/static/(.*)',   	'static',
		'/(.*)',          	'node',
		)

class favicon:
	def GET(self):
		return open(str("static/favicon.ico"), 'r').read()

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


class wiki():
	#def get_menu(self):
		#path = self.current_dir
		## De momento sólo muestro un nivel de CATEGORÍAS
		#data_dirs = [{'title': os.path.basename(d), 'path': d} 
					#for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
		#return data_dirs

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
					{'title': self.delete_extension(f), 
					'path': os.path.join(self.current_dir,f),
					'url': self.delete_extension(os.path.join("/", self.current_page['url'], f)),
					} for f in os.listdir(self.current_dir) 
			if self.is_page(os.path.join(self.current_dir, f))]
		return data_pages

	@staticmethod
	def is_page(filename, extension = EXTENSION):
		try:
			ext = filename.split('.')[-1]
			return ext == extension
		except ValueError:
			return False

	@staticmethod
	def delete_extension(filename):
		return os.path.splitext(filename)[0]

	def up_button(self):
		return "<a href=\"/"+os.path.dirname(self.current_page['url'])+"\">Up</a>"

	def new_page(self, url, content):
		f = open(os.path.join(DATA_DIR, str(url) + "." + EXTENSION), 'w')
		f.write(content.encode('utf-8'))

	def get_head(self):
		return render.head()

class node(wiki):
	def GET(self, page_url):
		self.current_page = {}
		self.current_page['url'] = str(page_url)
		self.current_page['title'] = os.path.basename(str(page_url))
		self.current_page['path'] = os.path.join(DATA_DIR, self.current_page['url'])
		#try:
		if os.path.isdir(self.current_page['path']):
			self.current_dir = self.current_page['path']
			html = str(render.head()) + str(render.dir(self))
			return html
		else:
			self.current_dir = os.path.dirname(self.current_page['path'])
			self.current_page['path'] = os.path.join(self.current_page['path'] + 
					"." + EXTENSION)
			html = str(render.head()) + str(render.page(self))
			return html
		#except:
			#return render.notfound()



class new(wiki):
	def not_page_exists(url):
		return not (os.path.isdir(os.path.join(DATA_DIR, url)) or
				os.path.exists(os.path.join(DATA_DIR, url + "." + EXTENSION)))

	page_exists_validator = web.form.Validator('Page already exists', 
		not_page_exists)

	form = web.form.Form(
        web.form.Textbox('url', web.form.notnull, page_exists_validator,
            size=30,
            description="Location:"),
        #web.form.Textbox('title', web.form.notnull, 
            #size=30,
            #description="Page title:"),
        web.form.Textarea('content', web.form.notnull, 
            rows=30, cols=80,
            description="Page content:", post="Use markdown syntax"),
        web.form.Button('Create page'),
    )

	def GET(self):
		url = web.input(url='').url
		form = self.form()
		form.fill({'url':url})
		return str(render.head()) + str(render.new(form))

	def POST(self):
		form = self.form()
		if not form.validates():
			return render.new(form)
		self.new_page(form.d.url, form.d.content)
		raise web.seeother('/' + form.d.url)

class static:
	def GET(self, filename=None):
		print("Hello world ==================== ")
		print self
		return open(str(filename), 'r').read()

if __name__ == "__main__": 
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()


