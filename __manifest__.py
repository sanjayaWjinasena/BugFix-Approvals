# -*- coding: utf-8 -*-
{
    'name': 'Jinasena : Module : Approvals',
    'version': '17.0.0.0.12',
    'summary': 'Studio-ported approval rules (75) + supporting security groups (15)',
    'author': 'Jinasena Agricultural Machinery (Pvt) Ltd.',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    # approval_rules.xml references these upstream models via search-domain
    # on model_id (maintenance.request, mrp.production, purchase.order, sale.order)
    # + studio.approval.rule from web_studio. Cascade-upgrade traversal loads
    # modules strictly in topological order so these must be dep-declared
    # or the model isn't yet in registry.models when this data file runs.
    # Do NOT depend on studio_customization — Odoo SH does not ship a manifest for it.
    'depends': [
        'base_setup', 'base_automation', 'web_studio',
        'maintenance', 'mrp', 'purchase', 'sale',
    ],
    'data': [
        # groups first: approval_rules.xml now references them via group_id (v0.0.11)
        'data/groups.xml',
        'data/approval_rules.xml',
    ],
    # Adopts the existing Studio groups/rules on databases that still have them (v0.0.12).
    'pre_init_hook': 'pre_init_hook',
    'installable': True,
    'auto_install': False,
    'application': True,
}
