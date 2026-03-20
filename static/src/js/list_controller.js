/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";
import { onWillStart } from "@odoo/owl";
import { loadSmAccessRules, findModelRule, getGlobalSettings } from "@sm_access_management/js/access_service";

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);

        onWillStart(async () => {
            await loadSmAccessRules();
            const modelName = this.props.resModel;
            const modelRule = findModelRule(modelName);
            const globalSettings = getGlobalSettings();

            // Global read-only
            if (globalSettings.make_readonly) {
                this.activeActions = { ...this.activeActions, create: false, edit: false, delete: false };
                this.editable = false;
            }

            if (!modelRule) return;

            if (modelRule.hide_create) {
                this.activeActions = { ...this.activeActions, create: false };
            }
            if (modelRule.hide_edit) {
                this.editable = false;
                this.activeActions = { ...this.activeActions, edit: false };
            }
        });
    },

    getStaticActionMenuItems() {
        const menuItems = super.getStaticActionMenuItems(...arguments);
        const modelName = this.props.resModel;
        const modelRule = findModelRule(modelName);
        const globalSettings = getGlobalSettings();

        if (globalSettings.make_readonly) {
            for (const key of ["archive", "unarchive", "duplicate", "delete"]) {
                if (menuItems[key]) menuItems[key].isAvailable = () => false;
            }
        }

        // Hide export from action menu
        if ((modelRule && modelRule.hide_export) || globalSettings.hide_export_global) {
            if (menuItems.export) menuItems.export.isAvailable = () => false;
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

        return menuItems;
    },

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
