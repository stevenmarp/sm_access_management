# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SmMenuRule(models.Model):
    """Hide specific menus and submenus per group."""
    _name = "sm.menu.rule"
    _description = "Menu Access Rule"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    menu_id = fields.Many2one(
        "ir.ui.menu", string="Menu", required=True,
        ondelete="cascade",
    )
    menu_full_name = fields.Char(
        string="Menu Path",
        compute="_compute_menu_full_name", store=True,
    )
    group_ids = fields.Many2many(
        "res.groups", "sm_menu_rule_group_rel", "rule_id", "group_id",
        string="Apply to Groups",
        help="Leave empty = hidden for ALL users.",
    )
    company_id = fields.Many2one(
        "res.company", string="Company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)
    note = fields.Text("Notes")

    @api.depends("menu_id", "menu_id.complete_name")
    def _compute_menu_full_name(self):
        for rec in self:
            rec.menu_full_name = rec.menu_id.complete_name or rec.menu_id.name or ""

    @api.depends("menu_id", "group_ids")
    def _compute_display_name(self):
        for rec in self:
            menu = rec.menu_full_name or rec.menu_id.name or "?"
            groups = ", ".join(rec.group_ids.mapped("name")) if rec.group_ids else _("All Users")
            rec.display_name = f"{menu} → {groups}"

    def _clear_menu_cache(self):
        """Clear ir.ui.menu cache so changes take effect immediately."""
        self.env.registry.clear_cache()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._clear_menu_cache()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._clear_menu_cache()
        return res

    def unlink(self):
        self._clear_menu_cache()
        return super().unlink()
