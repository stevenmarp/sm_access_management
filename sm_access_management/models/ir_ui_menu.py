# -*- coding: utf-8 -*-
from odoo import api, models


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    @api.model
    def _visible_menu_ids(self, debug=False):
        """Override to remove menus hidden by sm.menu.rule."""
        visible = super()._visible_menu_ids(debug=debug)

        user = self.env.user
        Rule = self.env["sm.menu.rule"].sudo()
        domain = [
            ("active", "=", True),
            "|", ("company_id", "=", False),
            ("company_id", "=", user.company_id.id),
        ]
        rules = Rule.search(domain)
        user_groups = user.groups_id

        hidden_ids = set()
        for rule in rules:
            if not rule.group_ids or (rule.group_ids & user_groups):
                hidden_ids.add(rule.menu_id.id)

        if hidden_ids:
            visible -= hidden_ids

        return visible
