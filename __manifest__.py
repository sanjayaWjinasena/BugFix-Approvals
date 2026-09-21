# -*- coding: utf-8 -*-
{
    'name': 'Jinasena : Module : Approvals',
    'version': '17.0.0.0.8',
    'summary': 'Studio-ported approval rules (75) + supporting security groups (15)',
    'author': 'Jinasena Agricultural Machinery (Pvt) Ltd.',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    # web_studio ships the studio.approval.rule model our approval_rules.xml
    # references. Without this explicit dep, cascade-upgrade traversals can
    # load this module before web_studio -> KeyError('studio.approval.rule').
    # Do NOT depend on studio_customization — Odoo SH does not ship a manifest for it.
    'depends': ['base_setup', 'base_automation', 'web_studio'],
    'data': [
        'data/approval_rules.xml',
        'data/groups.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
