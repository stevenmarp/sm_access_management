/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardActionServiceProps } from "@web/webclient/actions/action_service";
import { Component, onWillStart, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";

class SmAccessDashboard extends Component {
    static template = "sm_access_management.Dashboard";
    static props = { ...standardActionServiceProps };

    setup() {
        this.actionService = useService("action");
        this.state = useState({
            data: null,
            loading: true,
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        this.state.loading = true;
        try {
            this.state.data = await rpc("/sm_access_management/dashboard/data", {});
        } catch (e) {
            console.error("[SM Access] Dashboard error:", e);
            this.state.data = null;
        }
        this.state.loading = false;
    }

    openRules(modelName, actionXmlId) {
        this.actionService.doAction(actionXmlId);
    }

    openModelAccess() {
        this.actionService.doAction("sm_access_management.sm_access_rule_action");
    }
    openFieldAccess() {
        this.actionService.doAction("sm_access_management.sm_field_rule_action");
    }
    openMenuAccess() {
        this.actionService.doAction("sm_access_management.sm_menu_rule_action");
    }
    openButtonAccess() {
        this.actionService.doAction("sm_access_management.sm_button_rule_action");
    }
    openChatterAccess() {
        this.actionService.doAction("sm_access_management.sm_chatter_rule_action");
    }
    openFilterAccess() {
        this.actionService.doAction("sm_access_management.sm_filter_rule_action");
    }
    openGlobalAccess() {
        this.actionService.doAction("sm_access_management.sm_global_rule_action");
    }
    openDomainAccess() {
        this.actionService.doAction("sm_access_management.sm_domain_rule_action");
    }
}

registry.category("actions").add("sm_access_dashboard", SmAccessDashboard);
