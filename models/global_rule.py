# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SmGlobalRule(models.Model):
    """Global settings per group: disable debug mode, make user read-only,
    hide specific reports/actions globally."""
    _name = "sm.global.rule"
    _description = "Global Access Rule"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(compute="_compute_name", store=True)
    group_ids = fields.Many2many(
        "res.groups", "sm_global_rule_group_rel", "rule_id", "group_id",
        string="Apply to Groups",
        help="Leave empty = applies to ALL users (careful!).",
    )
    company_id = fields.Many2one(
        "res.company", string="Company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)

    # Global toggles
    disable_debug = fields.Boolean(
        "Disable Developer Mode",
        help="Prevent users from activating debug mode.",
    )
    make_readonly = fields.Boolean(
        "Read-Only User",
        help="Make the user completely read-only across ALL models. "
             "They can view records but cannot create, edit, or delete anything.",
    )
    disable_install_module = fields.Boolean(
        "Disable Module Install/Update",
        help="Prevent users from installing or updating modules.",
    )
    hide_import_global = fields.Boolean(
        "Hide Import (Global)",
        help="Hide the Import button on ALL list views.",
    )
    hide_export_global = fields.Boolean(
        "Hide Export (Global)",
        help="Hide the Export option on ALL list views.",
    )
    hide_spreadsheet_global = fields.Boolean(
        "Hide Spreadsheet (Global)",
        help="Hide the Insert in Spreadsheet option globally.",
    )
    hide_chatter_global = fields.Boolean(
        "Hide Chatter (Global)",
        help="Hide chatter on ALL models.",
    )
    hide_property_global = fields.Boolean(
        "Hide Properties (Global)",
        help="Hide Add Properties button on ALL models.",
    )

    # Restrict specific reports/actions
    restricted_action_ids = fields.Many2many(
        "ir.actions.act_window", "sm_global_rule_action_rel",
        "rule_id", "action_id",
        string="Hide Actions",
        help="Select specific window actions to hide from users.",
    )
    restricted_report_ids = fields.Many2many(
        "ir.actions.report", "sm_global_rule_report_rel",
        "rule_id", "report_id",
        string="Hide Reports",
        help="Select specific reports to hide from the Print menu.",
    )

    note = fields.Text("Notes")

    @api.depends("group_ids")
    def _compute_name(self):
        for rec in self:
            groups = ", ".join(rec.group_ids.mapped("name")) if rec.group_ids else _("All Users")
            rec.name = f"Global → {groups}"
