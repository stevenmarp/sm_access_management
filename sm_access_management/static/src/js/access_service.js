/** @odoo-module **/
/**
 * Central access service: loads all SM access rules once per session,
 * caches them, and provides lookup helpers for all JS patches.
 */
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

let _cache = null;
let _promise = null;

export async function loadSmAccessRules() {
    if (_cache !== null) {
        return _cache;
    }
    if (!_promise) {
        _promise = rpc("/web/dataset/call_kw/res.users/get_sm_access_rules", {
            model: "res.users",
            method: "get_sm_access_rules",
            args: [],
            kwargs: {},
        }).then((result) => {
            _cache = result || {};
            return _cache;
        }).catch((err) => {
            console.warn("[SM Access] Failed to load rules:", err);
            _promise = null;
            return {};
        });
    }
    return _promise;
}

export function getSmAccessCache() {
    return _cache || {};
}

/**
 * Find model access rule for a given model name.
 */
export function findModelRule(modelName) {
    if (!_cache || !_cache.model_access) return null;
    return _cache.model_access.find((r) => r.model === modelName) || null;
}

/**
 * Find field rules for a given model.
 */
export function findFieldRules(modelName) {
    if (!_cache || !_cache.field_access) return [];
    return _cache.field_access.filter((r) => r.model === modelName);
}

/**
 * Get ALL field rules (all models).
 */
export function getAllFieldRules() {
    if (!_cache || !_cache.field_access) return [];
    return _cache.field_access;
}

/**
 * Find chatter rule for a given model.
 */
export function findChatterRule(modelName) {
    if (!_cache || !_cache.chatter_access) return null;
    return _cache.chatter_access.find((r) => r.model === modelName) || null;
}

/**
 * Find button/tab rules for a given model.
 */
export function findButtonRules(modelName) {
    if (!_cache || !_cache.button_access) return [];
    return _cache.button_access.filter((r) => r.model === modelName);
}

/**
 * Find filter/groupby rules for a given model.
 */
export function findFilterRules(modelName) {
    if (!_cache || !_cache.filter_access) return [];
    return _cache.filter_access.filter((r) => r.model === modelName);
}

/**
 * Get global settings.
 */
export function getGlobalSettings() {
    if (!_cache || !_cache.global_settings) {
        return {
            disable_debug: false, make_readonly: false,
            disable_install_module: false,
            hide_import_global: false, hide_export_global: false,
            hide_spreadsheet_global: false,
            hide_chatter_global: false, hide_property_global: false,
            hidden_action_ids: [], hidden_report_ids: [],
        };
    }
    return _cache.global_settings;
}

/**
 * Get domain rules for a given model.
 */
export function findDomainRules(modelName) {
    if (!_cache || !_cache.domain_access) return [];
    return _cache.domain_access.filter((r) => r.model === modelName);
}

/**
 * Get hidden menu IDs.
 */
export function getHiddenMenuIds() {
    if (!_cache || !_cache.hidden_menu_ids) return [];
    return _cache.hidden_menu_ids;
}

/**
 * Clear cache (e.g., after rule change).
 */
export function clearSmAccessCache() {
    _cache = null;
    _promise = null;
}
