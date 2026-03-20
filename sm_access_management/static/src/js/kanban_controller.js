/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { onWillStart } from "@odoo/owl";
import { loadSmAccessRules, findModelRule, getGlobalSettings } from "@sm_access_management/js/access_service";

patch(KanbanController.prototype, {
    setup() {
        super.setup(...arguments);
        onWillStart(() => loadSmAccessRules());
    },

    get canCreate() {
        const originalResult = super.canCreate;
        const globalSettings = getGlobalSettings();

        if (globalSettings.make_readonly) {
            return false;
        }

        const modelName = this.props.resModel;
        const modelRule = findModelRule(modelName);

        if (modelRule && modelRule.hide_create) {
            return false;
        }

        return originalResult;
    },
});
