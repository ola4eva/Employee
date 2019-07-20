from odoo import api, fields, models


@api.model
def location_name_search(self, name='', args=None, operator='ilike', limit=100):
    if args is None:
        args = []
    records = self.browse()
    if len(name) == 2:
        records = self.search([('code', 'ilike', name)] + args, limit=limit)

    search_domain = [('name', operator, name)]
    if records:
        search_domain.append(('id', 'not in', records.ids))
    records += self.search(search_domain + args, limit=limit)
    # the field 'display_name' calls name_get() to get its value
    return [(record.id, record.display_name) for record in records]


class Designation(models.Model):
    _name = 'hr.employee.designation'
    _description = "Employee designation"
    _order = 'code' 
    name = fields.Char(string='Designation', required=True,
               help='Designation of Employees. E.g. Director, Deputy Director, etcetera.')
    code = fields.Char(string='Designation Code', help='Designation code.', required=True)

    name_search = location_name_search

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'The code of the designation must be unique!')
    ]


class Employee(models.Model):
    """This body of code add the constituency field to the hr.employee model"""
    _inherit = 'hr.employee'
    designation_id = fields.Many2one('hr.employee.designation', string='Designation')
