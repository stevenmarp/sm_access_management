# -*- coding: utf-8 -*-
from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        """Inject sm_access_disable_debug into session info so the
        JS frontend can disable debug mode before any page renders."""
        res = super().session_info()
        user = self.env.user
        if user and not user._is_superuser():
            Rule = self.env["sm.global.rule"].sudo()
            domain = [
                ("active", "=", True),
                ("disable_debug", "=", True),
                "|", ("company_id", "=", False),
                ("company_id", "=", user.company_id.id),
            ]
            rules = Rule.search(domain, limit=1)
            user_groups = user.all_group_ids
            for rule in rules:
                if not rule.group_ids or (rule.group_ids & user_groups):
                    res["sm_disable_debug"] = True
                    break
            else:
                res["sm_disable_debug"] = False
        return res
