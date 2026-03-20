# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def get_sm_access_rules(self):
        """Return ALL applicable access rules for the current user.
        Called once from JS on page load, cached client-side.
        Returns a dict with all rule types."""
        user = self.env.user
        company_domain = [
            ("active", "=", True),
            "|", ("company_id", "=", False),
            ("company_id", "=", user.company_id.id),
        ]
        user_groups = user.groups_id

        def _filter_by_group(rules):
            """Keep only rules that apply to current user (no groups = all users)."""
            result = []
            for r in rules:
                if not r.group_ids or (r.group_ids & user_groups):
                    result.append(r)
            return result

        # 1) MODEL ACCESS RULES
        access_rules = _filter_by_group(
            self.env["sm.access.rule"].sudo().search(company_domain)
        )
        model_access = {}
        for r in access_rules:
            m = r.model_name
            if m not in model_access:
                model_access[m] = {
                    "model": m,
                    "hide_archive": False, "hide_unarchive": False,
                    "hide_duplicate": False, "hide_delete": False,
                    "hide_create": False, "hide_edit": False,
                    "hide_import": False, "hide_export": False,
                    "hide_property": False, "hide_spreadsheet": False,
                }
            e = model_access[m]
            e["hide_archive"] = e["hide_archive"] or r.hide_archive
            e["hide_unarchive"] = e["hide_unarchive"] or r.hide_unarchive
            e["hide_duplicate"] = e["hide_duplicate"] or r.hide_duplicate
            e["hide_delete"] = e["hide_delete"] or r.hide_delete
            e["hide_create"] = e["hide_create"] or r.hide_create
            e["hide_edit"] = e["hide_edit"] or r.hide_edit
            e["hide_import"] = e["hide_import"] or r.hide_import
            e["hide_export"] = e["hide_export"] or r.hide_export
            e["hide_property"] = e["hide_property"] or r.hide_property
            e["hide_spreadsheet"] = e["hide_spreadsheet"] or r.hide_spreadsheet

        # 2) FIELD RULES
        field_rules = _filter_by_group(
            self.env["sm.field.rule"].sudo().search(company_domain)
        )
        field_access = {}
        for r in field_rules:
            key = f"{r.model_name}.{r.field_name}"
            if key not in field_access:
                field_access[key] = {
                    "model": r.model_name,
                    "field": r.field_name,
                    "invisible": False,
                    "readonly": False,
                    "required": False,
                    "remove_link": False,
                }
            e = field_access[key]
            e["invisible"] = e["invisible"] or r.make_invisible
            e["readonly"] = e["readonly"] or r.make_readonly
            e["required"] = e["required"] or r.make_required
            e["remove_link"] = e["remove_link"] or r.remove_external_link

        # 3) MENU RULES → list of hidden menu IDs
        menu_rules = _filter_by_group(
            self.env["sm.menu.rule"].sudo().search(company_domain)
        )
        hidden_menu_ids = list(set(r.menu_id.id for r in menu_rules))

        # 4) BUTTON/TAB RULES
        button_rules = _filter_by_group(
            self.env["sm.button.rule"].sudo().search(company_domain)
        )
        button_access = []
        for r in button_rules:
            button_access.append({
                "model": r.model_name,
                "type": r.target_type,
                "button_name": r.button_name or "",
                "tab_string": r.tab_string or "",
            })

        # 5) CHATTER RULES
        chatter_rules = _filter_by_group(
            self.env["sm.chatter.rule"].sudo().search(company_domain)
        )
        chatter_access = {}
        for r in chatter_rules:
            m = r.model_name
            if m not in chatter_access:
                chatter_access[m] = {
                    "model": m,
                    "hide_chatter": False,
                    "hide_send_message": False,
                    "hide_log_note": False,
                    "hide_activities": False,
                    "hide_followers": False,
                    "hide_scheduled": False,
                }
            e = chatter_access[m]
            e["hide_chatter"] = e["hide_chatter"] or r.hide_chatter
            e["hide_send_message"] = e["hide_send_message"] or r.hide_send_message
            e["hide_log_note"] = e["hide_log_note"] or r.hide_log_note
            e["hide_activities"] = e["hide_activities"] or r.hide_activities
            e["hide_followers"] = e["hide_followers"] or r.hide_followers
            e["hide_scheduled"] = e["hide_scheduled"] or r.hide_scheduled_messages

        # 6) FILTER RULES
        filter_rules = _filter_by_group(
            self.env["sm.filter.rule"].sudo().search(company_domain)
        )
        filter_access = []
        for r in filter_rules:
            filter_access.append({
                "model": r.model_name,
                "type": r.target_type,
                "name": r.filter_name or "",
            })

        # 7) GLOBAL RULES
        global_rules = _filter_by_group(
            self.env["sm.global.rule"].sudo().search(company_domain)
        )
        global_settings = {
            "disable_debug": False,
            "make_readonly": False,
            "disable_install_module": False,
            "hide_import_global": False,
            "hide_export_global": False,
            "hide_spreadsheet_global": False,
            "hide_chatter_global": False,
            "hide_property_global": False,
            "hidden_action_ids": [],
            "hidden_report_ids": [],
        }
        for r in global_rules:
            global_settings["disable_debug"] = global_settings["disable_debug"] or r.disable_debug
            global_settings["make_readonly"] = global_settings["make_readonly"] or r.make_readonly
            global_settings["disable_install_module"] = global_settings["disable_install_module"] or r.disable_install_module
            global_settings["hide_import_global"] = global_settings["hide_import_global"] or r.hide_import_global
            global_settings["hide_export_global"] = global_settings["hide_export_global"] or r.hide_export_global
            global_settings["hide_spreadsheet_global"] = global_settings["hide_spreadsheet_global"] or r.hide_spreadsheet_global
            global_settings["hide_chatter_global"] = global_settings["hide_chatter_global"] or r.hide_chatter_global
            global_settings["hide_property_global"] = global_settings["hide_property_global"] or r.hide_property_global
            global_settings["hidden_action_ids"].extend(r.restricted_action_ids.ids)
            global_settings["hidden_report_ids"].extend(r.restricted_report_ids.ids)
        global_settings["hidden_action_ids"] = list(set(global_settings["hidden_action_ids"]))
        global_settings["hidden_report_ids"] = list(set(global_settings["hidden_report_ids"]))

        # 8) DOMAIN RULES
        domain_rules = _filter_by_group(
            self.env["sm.domain.rule"].sudo().search(company_domain)
        )
        domain_access = []
        for r in domain_rules:
            domain_access.append({
                "model": r.model_name,
                "domain": r.domain or "[]",
                "restrict_create": r.restrict_create,
                "restrict_edit": r.restrict_edit,
                "restrict_delete": r.restrict_delete,
            })

        return {
            "model_access": list(model_access.values()),
            "field_access": list(field_access.values()),
            "hidden_menu_ids": hidden_menu_ids,
            "button_access": button_access,
            "chatter_access": list(chatter_access.values()),
            "filter_access": filter_access,
            "global_settings": global_settings,
            "domain_access": domain_access,
        }
