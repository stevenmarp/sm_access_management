/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { onWillStart, onMounted, onPatched } from "@odoo/owl";
import {
    loadSmAccessRules,
    findModelRule,
    findButtonRules,
    findFieldRules,
    getAllFieldRules,
    getGlobalSettings,
} from "@sm_access_management/js/access_service";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);

        onWillStart(async () => {
            await loadSmAccessRules();
            this._applySmModelRules();
        });

        onMounted(() => this._applySmDomRules());
        onPatched(() => this._applySmDomRules());
    },

    /**
     * Apply model-level rules (hide create/edit).
     * Runs after access rules are loaded.
     */
    _applySmModelRules() {
        const modelName = this.props.resModel;
        const modelRule = findModelRule(modelName);
        const globalSettings = getGlobalSettings();

        // Global read-only
        if (globalSettings.make_readonly) {
            this.canCreate = false;
            this.canEdit = false;
            if (this.archInfo && this.archInfo.activeActions) {
                this.archInfo.activeActions.edit = false;
            }
        }

        if (!modelRule) return;

        if (modelRule.hide_create) {
            this.canCreate = false;
        }
        if (modelRule.hide_edit) {
            this.canEdit = false;
            if (this.archInfo && this.archInfo.activeActions) {
                this.archInfo.activeActions.edit = false;
            }
        }
    },

    /**
     * Apply all DOM-based rules: hide buttons, tabs, invisible fields, external links.
     */
    _applySmDomRules() {
        const rootEl = this.rootRef && this.rootRef.el;
        if (!rootEl) return;

        const modelName = this.props.resModel;

        // --- Button / Tab hiding ---
        const buttonRules = findButtonRules(modelName);
        for (const rule of buttonRules) {
            if (rule.type === "button" && rule.button_name) {
                rootEl.querySelectorAll(
                    `button[name="${CSS.escape(rule.button_name)}"]`
                ).forEach((btn) => { btn.style.display = "none"; });
            } else if (rule.type === "stat_button" && rule.button_name) {
                rootEl.querySelectorAll(
                    `.oe_button_box .oe_stat_button[name="${CSS.escape(rule.button_name)}"],` +
                    `.oe_button_box button[name="${CSS.escape(rule.button_name)}"]`
                ).forEach((btn) => { btn.style.display = "none"; });
            } else if (rule.type === "tab" && rule.tab_string) {
                const tabLabel = rule.tab_string.trim().toLowerCase();
                rootEl.querySelectorAll(".o_notebook .nav-item .nav-link").forEach((link) => {
                    const text = (link.textContent || "").trim().toLowerCase();
                    const name = (link.getAttribute("name") || "").trim().toLowerCase();
                    if (text === tabLabel || name === tabLabel) {
                        link.closest(".nav-item").style.display = "none";
                    }
                });
            }
        }

        // --- Field invisible + remove external link (main model) ---
        const fieldRules = findFieldRules(modelName);
        this._applyFieldDomRules(rootEl, fieldRules);

        // --- Field invisible + remove external link (sub-models in one2many) ---
        const allRules = getAllFieldRules();
        const subModelRules = allRules.filter((r) => r.model !== modelName);
        // Group sub-model rules by field name for efficient DOM scanning
        for (const rule of subModelRules) {
            if (rule.invisible) {
                // Hide column in embedded list views (one2many)
                // th[data-name] = header, td.o_data_cell with matching index
                rootEl.querySelectorAll(
                    `th[data-name="${CSS.escape(rule.field)}"]`
                ).forEach((th) => {
                    const table = th.closest("table");
                    if (!table) return;
                    const colIndex = Array.from(th.parentElement.children).indexOf(th);
                    th.style.display = "none";
                    // Hide corresponding td in every row
                    table.querySelectorAll(`tbody tr`).forEach((row) => {
                        const td = row.children[colIndex];
                        if (td) td.style.display = "none";
                    });
                    // Also hide in tfoot if exists
                    table.querySelectorAll(`tfoot tr`).forEach((row) => {
                        const td = row.children[colIndex];
                        if (td) td.style.display = "none";
                    });
                });
            }
            if (rule.remove_link) {
                rootEl.querySelectorAll(
                    `.o_field_widget[name="${CSS.escape(rule.field)}"] .o_external_button`
                ).forEach((el) => { el.style.display = "none"; });
            }
        }
    },

    /**
     * Apply field DOM rules for fields on the main form (not in one2many).
     */
    _applyFieldDomRules(rootEl, fieldRules) {
        for (const rule of fieldRules) {
            if (rule.invisible) {
                rootEl.querySelectorAll(
                    `.o_field_widget[name="${CSS.escape(rule.field)}"]`
                ).forEach((el) => {
                    // Skip fields inside one2many list views
                    if (el.closest(".o_field_one2many, .o_list_view")) return;
                    const cell = el.closest(".o_cell");
                    if (cell) {
                        cell.style.display = "none";
                        const prev = cell.previousElementSibling;
                        if (prev && prev.classList.contains("o_cell") &&
                            prev.querySelector("label")) {
                            prev.style.display = "none";
                        }
                    } else {
                        el.style.display = "none";
                    }
                });
            }
            if (rule.remove_link) {
                rootEl.querySelectorAll(
                    `.o_field_widget[name="${CSS.escape(rule.field)}"] .o_external_button`
                ).forEach((el) => { el.style.display = "none"; });
            }
        }
    },

    getStaticActionMenuItems() {
        const menuItems = super.getStaticActionMenuItems(...arguments);
        const modelName = this.props.resModel;
        const modelRule = findModelRule(modelName);
        const globalSettings = getGlobalSettings();

        if (globalSettings.make_readonly) {
            for (const key of ["archive", "unarchive", "duplicate", "delete", "addPropertyFieldValue"]) {
                if (menuItems[key]) menuItems[key].isAvailable = () => false;
            }
            return menuItems;
        }

        if (!modelRule) return menuItems;

        if (modelRule.hide_archive && menuItems.archive) {
            menuItems.archive.isAvailable = () => false;
        }
        if (modelRule.hide_unarchive && menuItems.unarchive) {
            menuItems.unarchive.isAvailable = () => false;
        }
        if (modelRule.hide_duplicate && menuItems.duplicate) {
            menuItems.duplicate.isAvailable = () => false;
        }
        if (modelRule.hide_delete && menuItems.delete) {
            menuItems.delete.isAvailable = () => false;
        }
        if ((modelRule.hide_property || globalSettings.hide_property_global) && menuItems.addPropertyFieldValue) {
            menuItems.addPropertyFieldValue.isAvailable = () => false;
        }

        return menuItems;
    },

    /**
     * Override actionMenuItems to filter hidden reports/actions
     */
    get actionMenuItems() {
        const result = super.actionMenuItems;
        const globalSettings = getGlobalSettings();

        if (globalSettings.hidden_action_ids.length && result.action) {
            result.action = result.action.filter(
                (a) => !globalSettings.hidden_action_ids.includes(a.id)
            );
        }
        if (globalSettings.hidden_report_ids.length && result.print) {
            result.print = result.print.filter(
                (r) => !globalSettings.hidden_report_ids.includes(r.id)
            );
        }

        return result;
    },
});
