# -*- coding: utf-8 -*-
{
    'name': 'BugFix - Approvals',
    'version': '17.0.0.0.1',
    'summary': 'Studio-ported approval rules (75) + supporting security groups (15)',
    'author': 'Jinasena Agricultural Machinery (Pvt) Ltd.',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    # Do NOT depend on studio_customization — Odoo SH does not ship a manifest for it.
    'depends': ['base_setup', 'base_automation'],
    'data': ['data/approval_rules.xml', 'data/groups.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
