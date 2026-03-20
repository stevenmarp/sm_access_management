# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SmAccessRule(models.Model):
    """Model-level access rules: hide Archive, Delete, Duplicate, Create, Edit,
    Import, Export, Properties per model/group/company."""
    _name = "sm.access.rule"
    _description = "Model Access Rule"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(compute="_compute_name", store=True)
    model_id = fields.Many2one(
        "ir.model", string="Model", required=True,
        ondelete="cascade", domain=[("transient", "=", False)],
    )
    model_name = fields.Char(related="model_id.model", store=True, index=True)
    group_ids = fields.Many2many(
        "res.groups", "sm_access_rule_group_rel", "rule_id", "group_id",
        string="Apply to Groups",
        help="Leave empty = applies to ALL users.",
    )
    company_id = fields.Many2one(
        "res.company", string="Company",
        default=lambda self: self.env.company,
        help="Leave empty = all companies.",
    )
    active = fields.Boolean(default=True)

    # Model-level toggles
    hide_archive = fields.Boolean("Hide Archive")
    hide_unarchive = fields.Boolean("Hide Unarchive")
    hide_duplicate = fields.Boolean("Hide Duplicate")
    hide_delete = fields.Boolean("Hide Delete")
    hide_create = fields.Boolean("Hide Create")
    hide_edit = fields.Boolean("Hide Edit")
    hide_import = fields.Boolean("Hide Import")
    hide_export = fields.Boolean("Hide Export")
    hide_property = fields.Boolean("Hide Properties")
    hide_spreadsheet = fields.Boolean("Hide Spreadsheet")

    note = fields.Text("Notes")

    @api.depends("model_id", "group_ids")
    def _compute_name(self):
        for rec in self:
            model = rec.model_id.name or "?"
            groups = ", ".join(rec.group_ids.mapped("name")) if rec.group_ids else _("All Users")
            rec.name = f"{model} → {groups}"

    @api.constrains("model_id", "group_ids", "company_id")
    def _check_unique_rule(self):
        for rec in self:
            domain = [
                ("id", "!=", rec.id),
                ("model_id", "=", rec.model_id.id),
                ("company_id", "=", rec.company_id.id if rec.company_id else False),
            ]
            existing = self.search(domain)
            for other in existing:
                if not rec.group_ids and not other.group_ids:
                    raise ValidationError(
                        _("A rule for model '%s' with 'All Users' already exists.")
                        % rec.model_id.name
                    )
                if rec.group_ids & other.group_ids:
                    overlap = (rec.group_ids & other.group_ids).mapped("name")
                    raise ValidationError(
                        _("Overlapping groups [%s] for model '%s'.")
                        % (", ".join(overlap), rec.model_id.name)
                    )

    def action_toggle_all(self):
        for rec in self:
            new_val = not rec.hide_archive
            rec.write({
                "hide_archive": new_val, "hide_unarchive": new_val,
                "hide_duplicate": new_val, "hide_delete": new_val,
                "hide_create": new_val, "hide_edit": new_val,
                "hide_import": new_val, "hide_export": new_val,
                "hide_property": new_val, "hide_spreadsheet": new_val,
            })
