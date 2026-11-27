# -*- coding: utf-8 -*-
"""Let module upgrades re-load approval rules that already have approval entries.

web_studio's studio.approval.rule.write() raises
    "Rules with existing entries cannot be modified ..."
whenever vals CONTAIN group_id / model_id / method / action_id and any rule has
entries -- even when the values are identical. data/approval_rules.xml is not
noupdate, so every upgrade re-writes model_id and method on every rule, and the
first time someone uses an approval (e.g. rule 89, PO button_confirm) all later
upgrades fail.

Fix (v0.0.10, approved by the developer 2026-10-05): drop those keys from vals
when they equal the current value on every record being written. A real change
still reaches web_studio's guard and is still refused, exactly as Studio intends.
"""
from odoo import models

_GUARDED = ('group_id', 'model_id', 'method', 'action_id')


class StudioApprovalRule(models.Model):
    _inherit = 'studio.approval.rule'

    def write(self, vals):
        if self and any(k in vals for k in _GUARDED):
            vals = dict(vals)
            for key in _GUARDED:
                if key not in vals:
                    continue
                field = self._fields[key]
                new = vals[key]
                if field.type == 'many2one':
                    new = new or False
                    same = all((rec[key].id or False) == new for rec in self)
                else:
                    same = all((rec[key] or False) == (new or False) for rec in self)
                if same:
                    vals.pop(key)
        return super().write(vals)
