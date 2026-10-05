# -*- coding: utf-8 -*-
"""v0.0.11: let the corrected approver group reach rules that already have entries.

v0.0.11 restores group_id / domain / message on the approval rules (the port had
dropped them, so every rule defaulted to "User types / Internal User" with no
amount condition). web_studio refuses to change group_id on a rule that already
has approval entries ("archive the rule and create a new one instead").

Rule 89 (purchase.order button_confirm) has a test entry on the new install.
Following Studio's own guidance: archive the existing record, mark its name as
superseded and detach its xmlid. The data file then creates a fresh rule under
the same xmlid with the Clear-DB group and domain. The old record keeps its
entries for history. ORM only; no-op on fresh installs and when the group is
already correct.
"""
import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

RULES = {
    'BugFix-Approvals.rule_89_purchase_order_button_confirm_purchase_jin_po_approvers_po_a':
        'BugFix-Approvals.group_112_jin_po_approvers_po_amount_500_000',
}


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    for rule_xmlid, group_xmlid in RULES.items():
        rule = env.ref(rule_xmlid, raise_if_not_found=False)
        group = env.ref(group_xmlid, raise_if_not_found=False)
        if not rule or not group or rule.group_id == group or not rule.entry_ids:
            continue
        module, name = rule_xmlid.split('.', 1)
        env['ir.model.data'].search([('module', '=', module), ('name', '=', name)]).unlink()
        rule.write({'active': False, 'name': f'{rule.name} [superseded v0.0.11]'})
        _logger.info("BugFix-Approvals v0.0.11: archived approval rule %s (id %s, %d entries) "
                     "so it is recreated with group %s", rule_xmlid, rule.id, len(rule.entry_ids), group_xmlid)
