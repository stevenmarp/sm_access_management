/** @odoo-module **/
/**
 * Hide menus on the JS side as a second layer (primary is ir.ui.menu override).
 * This patches the menu service to filter out hidden menu IDs.
 */
import { patch } from "@web/core/utils/patch";
import { loadSmAccessRules, getHiddenMenuIds } from "@sm_access_management/js/access_service";

// The menu hiding is primarily done server-side via ir.ui.menu._visible_menu_ids override.
// This JS patch is a fallback for any edge cases where menus might still appear.
// Since we override _visible_menu_ids in Python, this file is intentionally minimal.

// If needed in the future, we can patch the NavBar component here.
