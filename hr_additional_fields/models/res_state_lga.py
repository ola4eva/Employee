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


class Lga(models.Model):
    _name = 'res.state.lga'
    _description = "Local Government Area"
    name = fields.Char(string='LGA', required=True, help='Local Governments e.g. Odo-Otin, Boluwaduro')
    state_id = fields.Many2one('res.country.state', "State")
    name_search = location_name_search
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The local government name must be unique!')
    ]


class Employee(models.Model):
    """This body of code add the constituency field to the hr.employee model"""
    _inherit = 'hr.employee'
    lga_id = fields.Many2one('res.state.lga', string='LGA', domain="[('state_id', '=',stateoforigin)]")
