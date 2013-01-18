import re, os
from collections import deque

class ArtichokeLiteral(object):
    def __init__(self, what):
        self.what = what

literal = ArtichokeLiteral

class ArtichokeTemplate(object):
    """
    Self contained template engine

    ArtichokeTemplate('''
    ${%def test(x):}
        <span>${x}</span>
    ${%end}
    <html>
        <head>
            <title>${title}</title>
        </head>
        <body>
            ${%for i in range(5):}
                ${%test(i)}
            ${%end}
        </body>
    </html>''').render({'title':'Hello < World'})
    """
    def __init__(self, text, minify=False):
        self.text = text
        self.compiled = None
        self.minify = minify

    def _parsed(self):
        padding = ''
        for line in self.text.split('\n'):
            if not self.minify:
                line += '\\n'

            for linepart, piece in enumerate(re.split(r'\$\{(.*?)\}', line)):
                if self.minify:
                    piece = piece.strip()
                    if not piece:
                        continue

                if linepart % 2:
                    #odd parts are inside the ${}
                    if piece.startswith('%'):
                        #starting with % are plain pieces of python
                        piece = piece[1:]
                        if piece == 'end':
                            #end tags just pop stack and are skipped
                            padding = padding[:-1]
                            continue

                        yield '%s%s' % (padding, piece)
                        if piece.split()[0] in ('if', 'for', 'def'):
                            padding += '\t'
                    else:
                        yield '%s__output__.append(escape(%s))' % (padding, piece)
                else:
                    #even parts are outside the ${} and are plain text
                    yield '%s__output__.append(u"%s")' % (padding, piece.replace('"', '\\"'))

    @property
    def _source(self):
        def wrap(code):
            yield 'def template():'
            for piece in code:
                yield '\t%s' % piece
            yield 'template()'
        return '\n'.join(wrap(self._parsed()))

    def _compile(self):
        self.compiled = compile(self._source, '', 'exec')
        return self._compile

    def _utilities(self, globals):
        def defined(what):
            return what in globals
        def literal(what):
            return ArtichokeLiteral(what)
        def escape(text):
            if isinstance(text, ArtichokeLiteral): return text.what
            return unicode(text).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')\
                                .replace('"','&quot;').replace("'",'&#039;')

        return {'defined':defined,
                'literal':literal,
                'escape':escape}

    def render(self, vars={}):
        if not self.compiled:
            self._compile()

        globals = {'__output__':deque()}
        globals.update(vars)
        globals.update(self._utilities(globals))
        eval(self.compiled, globals, {})
        return u''.join(globals['__output__']).encode('utf-8')

class ArtichokeTemplateLoader(object):
    def __init__(self, path, minify=False):
        self.path = path
        self.minify = minify

    def load(self, tmpl):
        if not tmpl.endswith('choke'):
            tmpl = tmpl + '.choke'

        f = open(os.path.join(self.path, tmpl))
        try:
            tmpl = ArtichokeTemplate(f.read(), self.minify)
            tmpl._compile()
            return tmpl
        finally:
            f.close()
