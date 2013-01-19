from operator import methodcaller



class Widget(object):
    def __init__(self, children=[], css_class="", **kw):
        super(Widget, self).__init__()
        self.children = children
        self.css_class = 'class="%s"' % css_class if css_class else ''

    def render_children(self):
        return '\n'.join(map(methodcaller('render'), self.children))

    def render(self):
        return self.render_children()


class Form(Widget):
    def __init__(self, children=[], css_class="", action="/", **kw):
        super(Form, self).__init__(children, css_class, **kw)
        self.action = action

    def render(self):
        form = """<form action="%(action)s" method="post" enctype="multipart/form-data" %(css_class)s >
    %(children)s
</form>""" % dict(action=self.action, css_class = self.css_class, children=self.render_children())
        return form


class Div(Widget):
    def render(self):
        div = """<div %(css_class)s >
    %(children)s
</div>""" % dict(css_class=self.css_class, children=self.render_children())
        return div


class InputField(Widget):
    template = '%(label)s<input type="%(type)s" name="%(name)s" %(value)s %(placeholder)s %(css_class)s />'

    def __init__(self, children=[], css_class="", name="", type="text", value="", label="", placeholder="", **kw):
        super(InputField, self).__init__(children, css_class, **kw)
        self.name = name
        self.label = label
        self.placeholder = placeholder
        self.type = type
        self.value = value

    def render(self):
        label = '<label>%s</label>\n' % self.label if self.label else ''
        placeholder = 'placeholder="%s"' % self.placeholder if self.placeholder else ''
        value = 'value="%s"' % self.value if self.value else ''
        return self.template % dict(label=label, type=self.type, name=self.name,
            value=value, placeholder=placeholder, css_class=self.css_class)

class TextArea(InputField):
    template = '%(label)s<textarea name="%(name)s" %(value)s %(placeholder)s %(css_class)s ></textarea>'

    def render(self):
        label = '<label>%s</label>\n' % self.label if self.label else ''
        placeholder = 'placeholder="%s"' % self.placeholder if self.placeholder else ''
        value = 'value="%s"' % self.value if self.value else ''
        return self.template % dict(label=label, name=self.name,
            value=value, placeholder=placeholder, css_class=self.css_class)



