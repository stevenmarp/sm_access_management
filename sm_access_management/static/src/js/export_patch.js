/** @odoo-module **/
/**
 * Hide Import / Export / Spreadsheet from cog menu based on model or global rules.
 *
 * In Odoo 18, Import/Export are registered in the cogMenu registry as separate
 * components. We patch their isDisplayed to respect SM Access rules.
 */
import { registry } from "@web/core/registry";
import { loadSmAccessRules, findModelRule, getGlobalSettings } from "@sm_access_management/js/access_service";

const cogMenuRegistry = registry.category("cogMenu");

/**
 * Wrap a cogMenu item's isDisplayed to add SM Access checks.
 * Uses registry.addEventListener to handle items added later.
 */
function patchCogMenuItem(registryKey, smCheckFn) {
    function tryPatch() {
        let item;
        try {
            item = cogMenuRegistry.get(registryKey);
        } catch (e) {
            return false; // Not registered yet
        }
        if (item.__sm_patched) return true; // Already patched

        const originalIsDisplayed = item.isDisplayed;
        item.isDisplayed = async (env) => {
            await loadSmAccessRules();
            if (smCheckFn(env)) return false;
            if (originalIsDisplayed) return originalIsDisplayed(env);
            return true;
        };
        item.__sm_patched = true;
        return true;
    }

    // Try immediately (in case already registered)
    if (!tryPatch()) {
        // Listen for future additions
        cogMenuRegistry.addEventListener("UPDATE", () => tryPatch());
    }
}

// ── Import Records (from base_import) ──
patchCogMenuItem("import-menu", (env) => {
    const globalSettings = getGlobalSettings();
    if (globalSettings.hide_import_global) return true;
    const modelRule = findModelRule(env.searchModel?.resModel);
    return !!(modelRule && modelRule.hide_import);
});

// ── Export All (from web core) ──
patchCogMenuItem("export-all-menu", (env) => {
    const globalSettings = getGlobalSettings();
    if (globalSettings.hide_export_global) return true;
    const modelRule = findModelRule(env.searchModel?.resModel);
    return !!(modelRule && modelRule.hide_export);
});

// ── Spreadsheet (from spreadsheet_edition enterprise module) ──
// Registry key is "spreadsheet-cog-menu" (NOT "insert_list_spreadsheet_menu")
patchCogMenuItem("spreadsheet-cog-menu", (env) => {
    const globalSettings = getGlobalSettings();
    if (globalSettings.hide_spreadsheet_global) return true;
    const modelRule = findModelRule(env.searchModel?.resModel);
    return !!(modelRule && modelRule.hide_spreadsheet);
});


