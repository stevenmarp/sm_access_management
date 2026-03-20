/** @odoo-module **/
/**
 * Patch the Chatter component to hide Send Message, Log Note, Activities, Followers.
 */
import { patch } from "@web/core/utils/patch";
import { Chatter } from "@mail/chatter/web_portal/chatter";
import { onWillStart } from "@odoo/owl";
import { loadSmAccessRules, findChatterRule, getGlobalSettings } from "@sm_access_management/js/access_service";

patch(Chatter.prototype, {
    setup() {
        super.setup(...arguments);
        onWillStart(() => loadSmAccessRules());
    },

    /**
     * Check if a chatter component should be hidden.
     */
    get smChatterRule() {
        const globalSettings = getGlobalSettings();
        if (globalSettings.hide_chatter_global) {
            return {
                hide_chatter: true,
                hide_send_message: true,
                hide_log_note: true,
                hide_activities: true,
                hide_followers: true,
                hide_scheduled: true,
            };
        }
        return findChatterRule(this.props.threadModel) || null;
    },

    get smHideChatter() {
        const rule = this.smChatterRule;
        return rule && rule.hide_chatter;
    },

    get smHideSendMessage() {
        const rule = this.smChatterRule;
        return rule && rule.hide_send_message;
    },

    get smHideLogNote() {
        const rule = this.smChatterRule;
        return rule && rule.hide_log_note;
    },

    get smHideActivities() {
        const rule = this.smChatterRule;
        return rule && rule.hide_activities;
    },

    get smHideFollowers() {
        const rule = this.smChatterRule;
        return rule && rule.hide_followers;
    },
});
