# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SmButtonRule(models.Model):
    """Hide specific buttons, stat buttons, or notebook tabs per model/group."""
    _name = "sm.button.rule"
    _description = "Button/Tab Access Rule"
    _order = "model_id, sequence"

    sequence = fields.Integer(default=10)
    model_id = fields.Many2one(
        "ir.model", string="Model", required=True,
        ondelete="cascade", domain=[("transient", "=", False)],
    )
    model_name = fields.Char(related="model_id.model", store=True, index=True)
    target_type = fields.Selection([
        ("button", "Button (Header/Status Bar)"),
        ("stat_button", "Stat Button (Smart Button)"),
        ("tab", "Notebook Tab"),
    ], string="What to Hide", required=True, default="button")
    button_name = fields.Char(
        "Button Name",
        help="The technical 'name' attribute of the button.\n\n"
             "How to find it:\n"
             "1. Open the form view with Developer Mode ON\n"
             "2. Right-click the button → Inspect Element\n"
             "3. Look for name=\"xxx\" in the <button> tag\n\n"
             "Examples: action_confirm, button_draft, action_cancel, "
             "action_quotation_send, action_view_invoice",
    )
    tab_string = fields.Char(
        "Tab Label",
        help="The visible label of the notebook tab.\n\n"
             "Examples: Other Info, Optional Products, Notes, "
             "Delivery, Invoicing",
    )
    group_ids = fields.Many2many(
        "res.groups", "sm_button_rule_group_rel", "rule_id", "group_id",
        string="Apply to Groups",
        help="Leave empty = applies to ALL users.",
    )
    company_id = fields.Many2one(
        "res.company", string="Company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)
    note = fields.Text("Notes")

    @api.depends("model_id", "target_type", "button_name", "tab_string")
    def _compute_display_name(self):
        for rec in self:
            model = rec.model_id.name or "?"
            if rec.target_type in ("button", "stat_button"):
                target = rec.button_name or "?"
                rec.display_name = f"{model}: hide button '{target}'"
            else:
                target = rec.tab_string or "?"
                rec.display_name = f"{model}: hide tab '{target}'"
