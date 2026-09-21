# -*- coding: utf-8 -*-
{
    'name': 'Jinasena : Module : Approvals',
    'version': '17.0.0.0.9',
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
        'data/approval_rules.xml',
        'data/groups.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
