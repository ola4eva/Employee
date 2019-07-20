# -*- coding: utf-8 -*-
from odoo import models, fields


class EmployeeGrade(models.Model):

    _name = 'emp.grade'
    _order = 'sequence,name'
    _description = 'Grade'

    name = fields.Char(string='Grade', required=True)
    sequence = fields.Integer(string="Integer")
    step_ids = fields.Many2many('emp.step', string="Steps")


class EmployeeStep(models.Model):
    """Steps under certain Grades"""

    _name = 'emp.step'
    _order = 'sequence,name'
    _description = 'Step'

    sequence = fields.Integer('Sequence')
    name = fields.Char(string='Step', required=True)
    grade_id = fields.Many2many('emp.grade', "Grade")
