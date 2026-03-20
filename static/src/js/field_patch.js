/** @odoo-module **/
/**
 * Patch the Field component to apply readonly/required rules.
 * Invisible fields + remove_external_link are handled via DOM in form_controller.js.
 */
import { patch } from "@web/core/utils/patch";
import { Field } from "@web/views/fields/field";
import { findFieldRules, getGlobalSettings } from "@sm_access_management/js/access_service";

/**
 * Patch Field to intercept readonly / required at fieldComponentProps level.
 * This works because Odoo 18 evaluates these at render time in the getter.
 */
patch(Field.prototype, {
    get fieldComponentProps() {
        const props = super.fieldComponentProps;

        const record = this.props.record;
        if (!record) return props;

        const modelName = record.resModel;
        const fieldName = this.props.name;
        const globalSettings = getGlobalSettings();

        // Global read-only → all fields readonly
        if (globalSettings.make_readonly) {
            props.readonly = true;
            return props;
        }

        const rules = findFieldRules(modelName);
        if (!rules.length) return props;

        const rule = rules.find((r) => r.field === fieldName);
        if (!rule) return props;

        if (rule.readonly) {
            props.readonly = true;
        }
        if (rule.required) {
            props.required = true;
        }

        return props;
    },
});
