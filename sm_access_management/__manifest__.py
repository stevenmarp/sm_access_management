# -*- coding: utf-8 -*-
# Copyright 2026 Steven Marp
{
    "name": "Access Management | Hide Menu, Fields, Buttons, Import, Export, Chatter",
    "version": "19.0.1.0.0",
    "summary": "Hide Fields, Menus, Buttons, Tabs, Chatter, Filters, Import/Export, Actions — per Model, per Group, per Company",
    "description": """
Access Management | All In One Access Rights Manager
======================================================

Complete access management solution for Odoo 19. Control what users can see
and do — all from one place, with just a few clicks. No coding required.

Features
--------
* **Model Access** — Hide Archive, Unarchive, Delete, Duplicate, Create, Edit, Import, Export, Spreadsheet, Properties per model per group
* **Field Access** — Make any field Invisible, Read-Only, or Required per model per group. Remove external link on Many2one fields
* **Menu Access** — Hide any menu or submenu per user group — server-side enforced
* **Button/Tab Access** — Hide any button (header, stat) or notebook tab per model per group
* **Filter/Group By Access** — Hide specific search filters and group-by options per model
* **Chatter Access** — Hide Send Message, Log Note, Activities, Followers, Scheduled Messages per model or globally
* **Import/Export/Spreadsheet** — Disable Import, Export, and/or Spreadsheet per model or globally
* **Domain Restrictions** — Restrict Create/Edit/Delete based on record field conditions
* **Disable Developer Mode** — Block debug mode for specific user groups
* **Read-Only User** — Make entire user read-only across all models
* **Disable Module Install/Update** — Prevent users from installing or updating modules
* **Restrict Reports/Actions** — Hide specific server actions and print reports from action menu
* **Hide Properties (Global)** — Remove "Add Property Field" option per model or globally
* **Dashboard** — Overview of all configured rules at a glance
* **Security Groups** — Manager and User roles for controlling who can manage access rules

Keywords: Access Management | Access Rights | Hide Fields | Hide Menus |
Hide Buttons | Hide Tabs | Hide Filters | Hide Chatter | Hide Activities |
Hide Import | Hide Export | Hide Archive | Hide Delete | Hide Duplicate |
Hide Create | Hide Edit | Read Only User | Readonly User | Disable Debug |
Disable Developer Mode | Field Permissions | Menu Permissions |
Button Permissions | Tab Permissions | Filter Permissions |
Restrict Actions | Restrict Reports | Domain Restrictions |
Per Model Access | Per Group Access | Per Company Access |
All In One Access | Access Manager | User Permissions |
Odoo Security | Action Menu Control | Fine-Grained Permissions |
Hide Action Menu | Model Access Control | Role Based Access |
Hide Properties | Remove Properties | Disable Properties |
Simplify Access | Access Control | User Access | Group Access |
Field Invisible | Field Readonly | Field Required |
Hide Sub Menu | Hide Navigation | Restrict Navigation |
Hide Chatter | Hide Send Message | Hide Log Note |
Hide Followers | Hide Activities | Chatter Access |
Import Export Control | Spreadsheet Control |
Hide Spreadsheet | Disable Module Install |
Remove External Link | Many2one Link |
Dashboard | Access Dashboard | Rules Overview |
Security Groups | Access Manager Role |
Company Wise Restrictions | Multi Company Access

Author: Steven Marp
    """,
    "author": "Steven Marp",
    "website": "https://apps.odoo.com/apps/browse?repo_maintainer_id=512936",
    "category": "Extra Tools",
    "license": "OPL-1",
    "depends": ["base", "web", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/access_rule_views.xml",
        "views/field_rule_views.xml",
        "views/menu_rule_views.xml",
        "views/button_rule_views.xml",
        "views/chatter_rule_views.xml",
        "views/filter_rule_views.xml",
        "views/global_rule_views.xml",
        "views/domain_rule_views.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sm_access_management/static/src/js/access_service.js",
            "sm_access_management/static/src/js/form_controller.js",
            "sm_access_management/static/src/js/list_controller.js",
            "sm_access_management/static/src/js/kanban_controller.js",
            "sm_access_management/static/src/js/chatter_patch.js",
            "sm_access_management/static/src/js/field_patch.js",
            "sm_access_management/static/src/js/menu_patch.js",
            "sm_access_management/static/src/js/debug_patch.js",
            "sm_access_management/static/src/js/export_patch.js",
            "sm_access_management/static/src/js/search_patch.js",
            "sm_access_management/static/src/xml/chatter_template.xml",
            "sm_access_management/static/src/dashboard/dashboard.js",
            "sm_access_management/static/src/dashboard/dashboard.xml",
            "sm_access_management/static/src/dashboard/dashboard.scss",
        ],
    },
    "images": ["static/description/banner.gif"],
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 269.00,
    "currency": "USD",
}
