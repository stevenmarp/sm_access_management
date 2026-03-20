# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class SmAccessDashboardController(http.Controller):

    @http.route("/sm_access_management/dashboard/data", type="json", auth="user")
    def dashboard_data(self, **kw):
        """Return dashboard statistics for all access rules."""
        env = request.env
        user = env.user
        company_id = user.company_id.id

        def _count(model, extra_domain=None):
            domain = [("active", "=", True)]
            if extra_domain:
                domain += extra_domain
            return env[model].sudo().search_count(domain)

        def _recent(model, limit=5):
            records = env[model].sudo().search(
                [("active", "=", True)], limit=limit, order="create_date desc"
            )
            result = []
            for r in records:
                vals = {"id": r.id, "name": r.display_name}
                if hasattr(r, "model_id"):
                    vals["model"] = r.model_id.name or ""
                if hasattr(r, "group_ids"):
                    vals["groups"] = ", ".join(r.group_ids.mapped("name")) or "All Users"
                result.append(vals)
            return result

        # Summary counts
        data = {
            "counts": {
                "model_access": _count("sm.access.rule"),
                "field_access": _count("sm.field.rule"),
                "menu_access": _count("sm.menu.rule"),
                "button_access": _count("sm.button.rule"),
                "chatter_access": _count("sm.chatter.rule"),
                "filter_access": _count("sm.filter.rule"),
                "global_access": _count("sm.global.rule"),
                "domain_access": _count("sm.domain.rule"),
            },
            "total_rules": 0,
            "total_models_affected": 0,
            "recent_model_rules": _recent("sm.access.rule"),
            "recent_field_rules": _recent("sm.field.rule"),
            "recent_menu_rules": _recent("sm.menu.rule"),
        }

        data["total_rules"] = sum(data["counts"].values())

        # Count unique models affected
        affected_models = set()
        for model_name in ["sm.access.rule", "sm.field.rule", "sm.button.rule",
                           "sm.chatter.rule", "sm.filter.rule", "sm.domain.rule"]:
            records = env[model_name].sudo().search([("active", "=", True)])
            for r in records:
                if hasattr(r, "model_name") and r.model_name:
                    affected_models.add(r.model_name)
        data["total_models_affected"] = len(affected_models)
        data["affected_models"] = sorted(list(affected_models))

        # Global settings summary
        global_rules = env["sm.global.rule"].sudo().search([("active", "=", True)])
        data["global_summary"] = {
            "debug_disabled": any(r.disable_debug for r in global_rules),
            "readonly_users": any(r.make_readonly for r in global_rules),
            "import_hidden": any(r.hide_import_global for r in global_rules),
            "export_hidden": any(r.hide_export_global for r in global_rules),
            "chatter_hidden": any(r.hide_chatter_global for r in global_rules),
        }

        return data
