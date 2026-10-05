# -*- coding: utf-8 -*-
"""Adopt existing Studio records on install (v0.0.12).

On a database that still carries the Studio customizations (an Odoo.sh staging
copy of production, for example) every group and approval rule this module
ships already exists, owned by studio_customization. Installing would then
either crash (res.groups unique name per category) or silently duplicate the
approval rules.

pre_init_hook runs before this module's data files load. For each record in
data/groups.xml and data/approval_rules.xml it looks for the matching existing
record and registers this module's xmlid on it, so the data files UPDATE the
existing record instead of creating a new one. Group memberships, approval
history (studio.approval.entry) and record ids are kept. The Studio xmlid stays
as well; when studio_customization is eventually uninstalled, Odoo keeps any
record that another module still references.

Matching (verified read-only against upgrade-testing-39206923, 2026-10-05):
  res.groups           name + category from the record's category_id search;
                       falls back to a unique name match (e.g. 'PR Approval',
                       whose category has no name).
  studio.approval.rule model + method + exact name; falls back to the Clear-DB
                       id in the trailing "(NN)" with the same model + method.
Records with no match (e.g. rules 91/92, absent on production) are created as
on a fresh database. On a fresh database nothing matches, so this is a no-op.

ORM only, no SQL.
"""
import ast
import logging
import os
import re

from lxml import etree

_logger = logging.getLogger(__name__)

MODULE = 'BugFix-Approvals'
_HERE = os.path.dirname(os.path.abspath(__file__))


def _records(filename):
    return etree.parse(os.path.join(_HERE, 'data', filename)).iter('record')


def _field(rec, name):
    return rec.find(f"field[@name='{name}']")


def _bind(env, xmlid, model, res_id):
    IMD = env['ir.model.data'].sudo()
    if IMD.search_count([('module', '=', MODULE), ('name', '=', xmlid)]):
        return False
    IMD.create({'module': MODULE, 'name': xmlid, 'model': model, 'res_id': res_id, 'noupdate': False})
    return True


def _adopt_groups(env):
    Groups = env['res.groups'].sudo().with_context(active_test=False)
    adopted = 0
    for rec in _records('groups.xml'):
        name = _field(rec, 'name').text
        cat = _field(rec, 'category_id')
        domain = [('name', '=', name)]
        if cat is not None and cat.get('search'):
            cats = env['ir.module.category'].sudo().search(ast.literal_eval(cat.get('search')))
            domain.append(('category_id', 'in', cats.ids))
        else:
            domain.append(('category_id', '=', False))
        hit = Groups.search(domain)
        if not hit:
            hit = Groups.search([('name', '=', name)])
        if len(hit) == 1 and _bind(env, rec.get('id'), 'res.groups', hit.id):
            adopted += 1
        elif len(hit) > 1:
            _logger.warning("%s: group %r ambiguous (%s), not adopted", MODULE, name, hit.ids)
    return adopted


def _adopt_rules(env):
    Rules = env['studio.approval.rule'].sudo().with_context(active_test=False)
    adopted = 0
    for rec in _records('approval_rules.xml'):
        name = _field(rec, 'name').text
        model = ast.literal_eval(_field(rec, 'model_id').get('search'))[0][2]
        method = _field(rec, 'method').text
        base = [('model_name', '=', model), ('method', '=', method)]
        hit = Rules.search(base + [('name', '=', name)])
        if len(hit) != 1:
            m = re.search(r'\((\d+)\)\s*$', name)
            hit = Rules.search(base + [('id', '=', int(m.group(1)))]) if m else Rules.browse()
        if len(hit) != 1:
            continue
        # web_studio forbids changing the group of a rule that has approval
        # entries. If the shipped group differs, follow Studio's own advice:
        # leave the old rule archived with its history and let the data file
        # create a fresh one.
        g = _field(rec, 'group_id')
        if g is not None and hit.entry_ids:
            want = env.ref(g.get('ref'), raise_if_not_found=False)
            if want and want != hit.group_id:
                hit.write({'active': False, 'name': f'{hit.name} [superseded by {MODULE}]'})
                _logger.info("%s: rule %s has entries and a different group; archived, new one will be created",
                             MODULE, hit.id)
                continue
        if _bind(env, rec.get('id'), 'studio.approval.rule', hit.id):
            adopted += 1
    return adopted


def pre_init_hook(env):
    groups = _adopt_groups(env)      # groups first: rules' group refs resolve through these xmlids
    rules = _adopt_rules(env)
    _logger.info("%s pre_init_hook: adopted %d existing groups and %d existing approval rules",
                 MODULE, groups, rules)
