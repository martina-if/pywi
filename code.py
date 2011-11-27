import web
import htmlize

urls = (
		'/',                'index',
		'/icons/(.*)',    	'static',
		'/static/(.*)',   	'static',
		'/(.*)',          	'page',
		)

t_globals = {
		'htmlize': htmlize.htmlize,
}

render = web.template.render('templates/', globals=t_globals)

class index:
    def GET(self):
		# Esto es para coger el nombre del QS
		#i = web.input(name=None)
		#return render.index(i.name)
		# Esco coge el nombre de la URL
		return render.index(name)

class page:
	def GET(self, page):
		return render.page(str(page))

class static:
	def GET(self, filename=None):
		print("KAKOTA==================== ")
		print self
		return open(str(filename), 'r').read()

if __name__ == "__main__": 
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()
