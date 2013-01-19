class FormBuilder(object):
    def __init__(self, action, fields, fields_order=None):
        self.fields = fields
        self.action = action

        if not fields_order:
            self.fields_order = self.fields.keys()
        else:
            self.fields_order = fields_order

    def render(self):
        form = ''
        form += '<form action="%(action)s" method="post" enctype="multipart/form-data">\n' % dict(action=self.action)
        form += '<table>\n'

        for field_name in self.fields_order:
            field_attrs = self.fields[field_name]

            form += '<tr>\n'
            form += '<td id="%s_label">%s</td>\n' % (field_name, field_attrs.get('label', '%s:' % field_name.capitalize()))
            form += '<td id="%s_field">' % field_name
            field_type = field_attrs.get('type', 'text')
            if field_type == 'textarea':
                form += '<textarea name="%s"></textarea>' % field_name
            else:
                form += '<input type="%s" name="%s"/>' % (field_type, field_name)
            form += '</td>\n'
            form += '</tr>\n'

        form += '''<tr>
                    <td id="submit_label"></td>
                    <td id="submit_field"><input type="submit" value="Submit"/></td>
                </tr>\n'''
        form += '</table>\n'
        form += '</form>\n'
        return form
