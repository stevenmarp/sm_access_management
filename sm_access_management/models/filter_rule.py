# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SmFilterRule(models.Model):
    """Hide specific search filters or group-by options per model/group."""
    _name = "sm.filter.rule"
    _description = "Filter Access Rule"
    _order = "model_id, sequence"

    sequence = fields.Integer(default=10)
    model_id = fields.Many2one(
        "ir.model", string="Model", required=True,
        ondelete="cascade", domain=[("transient", "=", False)],
    )
    model_name = fields.Char(related="model_id.model", store=True, index=True)
    target_type = fields.Selection([
        ("filter", "Filter"),
        ("groupby", "Group By"),
    ], string="Target Type", required=True, default="filter")
    filter_name = fields.Char(
        "Filter/GroupBy Name",
        help="The technical name attribute of the filter in the search view XML.",
    )
    filter_label = fields.Char(
        "Label (for reference)",
        help="Human-readable label for your reference.",
    )
    group_ids = fields.Many2many(
        "res.groups", "sm_filter_rule_group_rel", "rule_id", "group_id",
        string="Apply to Groups",
        help="Leave empty = hidden for ALL users.",
    )
    company_id = fields.Many2one(
        "res.company", string="Company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)
    note = fields.Text("Notes")

    @api.depends("model_id", "target_type", "filter_name")
    def _compute_display_name(self):
        for rec in self:
            model = rec.model_id.name or "?"
            rec.display_name = f"{model}: {rec.target_type} '{rec.filter_name or '?'}'"
