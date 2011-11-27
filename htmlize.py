# -*- coding: utf-8 -*-
from asciidocapi import AsciiDocAPI
import StringIO

def htmlize(filename):
	asciidoc = AsciiDocAPI('../asciidoc/asciidoc.py')
	outfile = StringIO.StringIO()
	asciidoc.options('--no-header-footer')
	#asciidoc.options.append('--attribute', 'linkcss=untroubled.css')
	asciidoc.execute(filename, outfile) #, backend='html5')
	return str(outfile.getvalue())
	
