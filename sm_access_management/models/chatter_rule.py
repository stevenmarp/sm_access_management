# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SmChatterRule(models.Model):
    """Hide chatter components per model/group: Send Message, Log Note, Activities, Followers."""
    _name = "sm.chatter.rule"
    _description = "Chatter Access Rule"
    _order = "model_id, sequence"

    sequence = fields.Integer(default=10)
    model_id = fields.Many2one(
        "ir.model", string="Model", required=True,
        ondelete="cascade",
        domain=[("transient", "=", False), ("is_mail_thread", "=", True)],
    )
    model_name = fields.Char(related="model_id.model", store=True, index=True)
    group_ids = fields.Many2many(
        "res.groups", "sm_chatter_rule_group_rel", "rule_id", "group_id",
        string="Apply to Groups",
        help="Leave empty = applies to ALL users.",
    )
    company_id = fields.Many2one(
        "res.company", string="Company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)

    # Chatter toggles
    hide_chatter = fields.Boolean("Hide Entire Chatter")
    hide_send_message = fields.Boolean("Hide Send Message")
    hide_log_note = fields.Boolean("Hide Log Note")
    hide_activities = fields.Boolean("Hide Activities")
    hide_followers = fields.Boolean("Hide Followers")
    hide_scheduled_messages = fields.Boolean("Hide Scheduled Messages")

    note = fields.Text("Notes")

    @api.depends("model_id", "group_ids")
    def _compute_display_name(self):
        for rec in self:
            model = rec.model_id.name or "?"
            groups = ", ".join(rec.group_ids.mapped("name")) if rec.group_ids else _("All Users")
            rec.display_name = f"{model} → {groups}"

