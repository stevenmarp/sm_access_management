# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SmDomainRule(models.Model):
    """Domain-based restrictions: conditionally restrict create/edit/delete
    based on field values (e.g. 'state = done' → readonly)."""
    _name = "sm.domain.rule"
    _description = "Domain-Based Access Rule"
    _order = "model_id, sequence"

    sequence = fields.Integer(default=10)
    model_id = fields.Many2one(
        "ir.model", string="Model", required=True,
        ondelete="cascade", domain=[("transient", "=", False)],
    )
    model_name = fields.Char(related="model_id.model", store=True, index=True)
    domain = fields.Char(
        "Domain (Condition)",
        required=True,
        default="[]",
        help="Python domain expression. When records match this domain, "
             "the restrictions below apply. E.g. [('state','=','done')]",
    )
    group_ids = fields.Many2many(
        "res.groups", "sm_domain_rule_group_rel", "rule_id", "group_id",
        string="Apply to Groups",
        help="Leave empty = applies to ALL users.",
    )
    company_id = fields.Many2one(
        "res.company", string="Company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)

    # Restrictions when domain matches
    restrict_create = fields.Boolean("Restrict Create")
    restrict_edit = fields.Boolean("Restrict Edit (Read-Only)")
    restrict_delete = fields.Boolean("Restrict Delete")

    note = fields.Text("Notes")

    @api.depends("model_id", "domain")
    def _compute_display_name(self):
        for rec in self:
            model = rec.model_id.name or "?"
            rec.display_name = f"{model}: {rec.domain}"
