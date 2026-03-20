/** @odoo-module **/
/**
 * Patch search model to hide specific filters and group-by options
 * based on sm.filter.rule configurations.
 */
import { patch } from "@web/core/utils/patch";
import { SearchModel } from "@web/search/search_model";
import { loadSmAccessRules, findFilterRules } from "@sm_access_management/js/access_service";

patch(SearchModel.prototype, {
    async load(config) {
        await super.load(config);
        await loadSmAccessRules();
        this._applySmFilterRules();
    },

    _applySmFilterRules() {
        const modelName = this.resModel;
        if (!modelName) return;

        const rules = findFilterRules(modelName);
        if (!rules.length) return;

        const hiddenFilters = rules
            .filter((r) => r.type === "filter")
            .map((r) => r.name);
        const hiddenGroupBys = rules
            .filter((r) => r.type === "groupby")
            .map((r) => r.name);

        if (!hiddenFilters.length && !hiddenGroupBys.length) return;

        // Remove matching searchItems
        for (const [id, item] of Object.entries(this.searchItems || {})) {
            if (!item) continue;
            if (item.type === "filter" && hiddenFilters.includes(item.name)) {
                delete this.searchItems[id];
            }
            if (item.type === "groupBy" && hiddenGroupBys.includes(item.fieldName || item.name)) {
                delete this.searchItems[id];
            }
        }
    },
});
