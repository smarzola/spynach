import jinja2

class SpynachTemplateLoader(object):
    def __init__(self, path, autoreload):
        self.jinja_environ = jinja2.Environment(loader=jinja2.FileSystemLoader(path), auto_reload=autoreload)

    def load(self, tmpl):
        if not tmpl.endswith('jinja'):
            tmpl += '.jinja'

        self.template = self.jinja_environ.get_template(tmpl)
        return self

    def render(self, tmpl_context):
        return self.template.render(tmpl_context).encode('utf8')
