# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from sqlalchemy.ext.declarative import declared_attr
from .associationproxy import association_proxy
from .categorization import Categorizable
from .mixins import (
    deferred, BusinessObject, Hierarchical, Timeboxed,
    )
from .object_document import Documentable
from .object_person import Personable
from .reflection import PublishOnly

CATEGORY_CONTROL_TYPE_ID = 100
CATEGORY_ASSERTION_TYPE_ID = 102

class ControlCategorized(Categorizable):
  @declared_attr
  def categorizations(cls):
    return cls._categorizations(
        'categorizations', 'categories', CATEGORY_CONTROL_TYPE_ID)

class AssertionCategorized(Categorizable):
  @declared_attr
  def assertations(cls):
    return cls._categorizations(
        'assertations', 'assertions', CATEGORY_ASSERTION_TYPE_ID)

class Control(
    BusinessObject, Documentable, Personable, ControlCategorized, AssertionCategorized,
    Hierarchical, Timeboxed, db.Model):
  __tablename__ = 'controls'

  company_control = deferred(db.Column(db.Boolean), 'Control')
  directive_id = deferred(
      db.Column(db.Integer, db.ForeignKey('directives.id')), 'Control')
  type_id = deferred(db.Column(db.Integer), 'Control')
  kind_id = deferred(db.Column(db.Integer), 'Control')
  means_id = deferred(db.Column(db.Integer), 'Control')
  version = deferred(db.Column(db.String), 'Control')
  documentation_description = deferred(db.Column(db.Text), 'Control')
  verify_frequency_id = deferred(db.Column(db.Integer), 'Control')
  fraud_related = deferred(db.Column(db.Boolean), 'Control')
  key_control = deferred(db.Column(db.Boolean), 'Control')
  active = deferred(db.Column(db.Boolean), 'Control')
  notes = deferred(db.Column(db.Text), 'Control')

  type = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Control.type_id) == Option.id, '\
                  'Option.role == "control_type")',
      uselist=False)
  kind = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Control.kind_id) == Option.id, '\
                  'Option.role == "control_kind")',
      uselist=False)
  means = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Control.means_id) == Option.id, '\
                  'Option.role == "control_means")',
      uselist=False)
  verify_frequency = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Control.verify_frequency_id) == Option.id, '\
                  'Option.role == "verify_frequency")',
      uselist=False)
  program_controls = db.relationship(
      'ProgramControl', backref='control', cascade='all, delete-orphan')
  programs = association_proxy(
      'program_controls', 'program', 'ProgramControl')
  system_controls = db.relationship(
      'SystemControl', backref='control', cascade='all, delete-orphan')
  systems = association_proxy(
      'system_controls', 'system', 'SystemControl')
  control_sections = db.relationship(
      'ControlSection', backref='control', cascade='all, delete-orphan')
  sections = association_proxy(
      'control_sections', 'section', 'ControlSection')
  objective_controls = db.relationship(
      'ObjectiveControl', backref='control', cascade='all, delete-orphan')
  objectives = association_proxy(
      'objective_controls', 'objective', 'ObjectiveControl')
  control_controls = db.relationship(
      'ControlControl',
      foreign_keys='ControlControl.control_id',
      backref='control',
      cascade='all, delete-orphan',
      )
  implemented_controls = association_proxy(
      'control_controls', 'implemented_control', 'ControlControl')
  implementing_control_controls = db.relationship(
      'ControlControl',
      foreign_keys='ControlControl.implemented_control_id',
      backref='implemented_control',
      cascade='all, delete-orphan',
      )
  implementing_controls = association_proxy(
      'implementing_control_controls', 'control', 'ControlControl')
  control_risks = db.relationship(
      'ControlRisk', backref='control', cascade='all, delete-orphan')
  risks = association_proxy('control_risks', 'risk', 'ControlRisk')
  control_assessments = db.relationship(
      'ControlAssessment', backref='control', cascade='all, delete-orphan')
  object_controls = db.relationship(
      'ObjectControl', backref='control', cascade='all, delete-orphan')

  # REST properties
  _publish_attrs = [
      'active',
      'categories',
      'assertions',
      'company_control',
      'control_assessments',
      'directive',
      'documentation_description',
      'fraud_related',
      'implemented_controls',
      'implementing_controls',
      'key_control',
      'kind',
      'means',
      'notes',
      'risks',
      'sections',
      'objectives',
      'programs',
      'systems',
      'type',
      'verify_frequency',
      'version',
      PublishOnly('control_controls'),
      PublishOnly('control_risks'),
      PublishOnly('control_sections'),
      PublishOnly('objective_controls'),
      PublishOnly('implementing_control_controls'),
      PublishOnly('system_controls'),
      PublishOnly('program_controls'),
      'object_controls',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm
    query = super(Control, cls).eager_query()
    return query.options(
        orm.joinedload('directive'),
        orm.joinedload('control_assessments'),
        orm.joinedload('control_controls'),
        orm.joinedload('implementing_control_controls'),
        orm.joinedload('control_risks'),
        orm.joinedload('control_sections'),
        orm.joinedload('objective_controls'),
        orm.joinedload('program_controls'),
        orm.joinedload('system_controls'),
        orm.joinedload('object_controls'),
        )
