from odoo import api, fields, models


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    name = fields.Char("Name")
    firstname = fields.Char("First Name")
    othername = fields.Char("Other Name")
    surname = fields.Char("Surname Name")
    job_id = fields.Many2one('hr.job', string="Rank")
    employee_title = fields.Many2one('res.partner.title', "Title")
    pension_id = fields.Char('Pension Details')
    ippis_no = fields.Char("IPPIS Number")
    fileno = fields.Char('File Number')
    fcsc_estab_no = fields.Char("FCSC/Estab No")

    # Grade id
    grade_id = fields.Many2one('emp.grade', string="Grade Level")
    step_id = fields.Many2one('emp.step', string="Step", domain="[('grade_id', '=', grade_id)]")

    # Appointments
    date_first_appointment = fields.Date('Date of First Appointment')
    date_present_appointment = fields.Date('Date of Present Appointment')
    date_confirm_appointment = fields.Date('Date of confirmation of Appointment')
    date_posted = fields.Date("Date Posted to Ministry of Env")

    # Retirement
    date_retirement = fields.Date('Date of Retirement', compute='_compute_date_of_retirement', store=True)
    education_ids = fields.One2many('educational.history', 'employee_id', String='Educational History')
    salary_grade_level = fields.Selection([
        ('one', 'Grade Level 1'),
        ('two', 'Grade Level 2'),
        ('three', 'Grade Level 3'),
        ('four', 'Grade Level 4'),
        ('five', 'Grade Level 5'),
        ('six', 'Grade Level 6'),
        ('seven', 'Grade Level 7'),
        ('eight', 'Grade Level 8'),
        ('nine', 'Grade Level 9'),
        ('ten', 'Grade Level 10'),
        ('eleven', 'Grade Level 11'),
        ('twelve', 'Grade Level 12'),
        ('thirteen', 'Grade Level 13'),
        ('fourteen', 'Grade Level 14'),
        ('fifteen', 'Grade Level 15'),
        ('sixteen', 'Grade Level 16'),
        ('seventeen', 'Grade Level 17')
    ], 'Salary Grade Level')

    country_id = fields.Many2one(
        default=lambda self: int(self.env['res.country'].search([('name', '=', "Nigeria"), ('code', '=', "NG")]))
    )
    stateoforigin = fields.Many2one('res.country.state', 'State Of Origin', domain="[('country_id', '=', country_id)]")
    full_resi_address = fields.Char('Full Residential Address')

    @api.onchange('firstname', 'othername', 'surname')
    def get_full_name(self):
        if self.firstname and self.othername and self.surname:
            self.name = self.firstname + " " + self.othername + " " + self.surname

    @api.one
    @api.depends('date_first_appointment', 'birthday')
    def _compute_date_of_retirement(self):
        """If only the birthday is supplied, calculate the date of retirement based on this field only.

        """
        if self.birthday:
            birthday_date = fields.Date.from_string(self.birthday)
            add_max_age = birthday_date.year + 60
            date_retirement_string1 = birthday_date.replace(year=add_max_age)
            self.date_retirement = fields.Date.to_string(date_retirement_string1)

        # Compute the date of retirement using only the date of first appointment
        # else if
        if self.date_first_appointment:
            appointment_date = fields.Date.from_string(self.date_first_appointment)
            add_year_of_service = appointment_date.year + 35
            date_retirement_string2 = appointment_date.replace(year=add_year_of_service)
            self.date_retirement = fields.Date.to_string(date_retirement_string2)

        # If both birthday and date of first appointment
        # else
        if self.birthday and self.date_first_appointment:
            if date_retirement_string1 < date_retirement_string2:
                self.date_retirement = fields.Date.to_string(date_retirement_string1)
            else:
                self.date_retirement = fields.Date.to_string(date_retirement_string2)


class educational_history(models.Model):

    _name = "educational.history"
    school_name = fields.Char('Name of Institution')
    date_from = fields.Date('From')
    date_to = fields.Date('To')
    cert_date = fields.Date('Qualifications Date', help="Date of Issuance of Certificate")
    quali = fields.Char('Qualification')
    course_studied = fields.Char('Course')
    employee_id = fields.Many2one('hr.employee', 'Employee')


class PensionManagers(models.Model):

    _name = 'pension.pfa'

    name = fields.Char("Pension Managers")
    street = fields.Char("Street")
    email = fields.Char("Email")


class PensionInfo(models.Model):

    _name = 'pension.information'

    pension_manager_id = fields.Many2one('pension.pfa', "Pension Manager")
    pension_number = fields.Char("Pension Number")
    beneficiary = fields.Char("Beneficiary")
