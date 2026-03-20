/** @odoo-module **/
/**
 * Disable developer mode for restricted users.
 * Uses session_info injected by ir.http override.
 */
import { session } from "@web/session";

// If the server injected sm_disable_debug, force-clear debug mode
if (session.sm_disable_debug) {
    // Clear debug from URL and odoo global
    odoo.debug = "";
    // Remove ?debug= from URL if present
    const url = new URL(window.location.href);
    if (url.searchParams.has("debug")) {
        url.searchParams.delete("debug");
        window.history.replaceState({}, "", url.toString());
    }
}
