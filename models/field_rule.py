# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SmFieldRule(models.Model):
    """Field-level access: make fields invisible, readonly, or required."""
    _name = "sm.field.rule"
    _description = "Field Access Rule"
    _order = "model_id, sequence"

    sequence = fields.Integer(default=10)
    model_id = fields.Many2one(
        "ir.model", string="Model", required=True,
        ondelete="cascade", domain=[("transient", "=", False)],
    )
    model_name = fields.Char(related="model_id.model", store=True, index=True)
    field_id = fields.Many2one(
        "ir.model.fields", string="Field", required=True,
        ondelete="cascade",
        domain="[('model_id', '=', model_id), ('ttype', 'not in', ['one2many'])]",
    )
    field_name = fields.Char(related="field_id.name", store=True)
    field_ttype = fields.Selection(related="field_id.ttype", store=True)
    group_ids = fields.Many2many(
        "res.groups", "sm_field_rule_group_rel", "rule_id", "group_id",
        string="Apply to Groups",
        help="Leave empty = applies to ALL users.",
    )
    company_id = fields.Many2one(
        "res.company", string="Company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)

    # Field-level access
    make_invisible = fields.Boolean("Invisible", help="Hide the field completely")
    make_readonly = fields.Boolean("Read-Only", help="User cannot edit this field")
    make_required = fields.Boolean("Required", help="Field becomes mandatory")
    remove_external_link = fields.Boolean(
        "Remove External Link",
        help="Remove the external link icon on Many2one fields",
    )

    note = fields.Text("Notes")

    @api.depends("model_id", "field_id", "group_ids")
    def _compute_display_name(self):
        for rec in self:
            model = rec.model_id.name or "?"
            field = rec.field_id.field_description or rec.field_name or "?"
            groups = ", ".join(rec.group_ids.mapped("name")) if rec.group_ids else _("All Users")
            rec.display_name = f"{model}.{field} → {groups}"
