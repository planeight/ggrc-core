# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for snapshot block converter."""

from cached_property import cached_property

from ggrc import models


class SnapshotBlockConverter(object):
  """Block converter for snapshots of a single object type."""

  def __init__(self, converter, ids):
    self.converter = converter
    self.ids = ids

  @staticmethod
  def handle_row_data():
    pass

  @property
  def name(self):
    return "{} Snapshot".format(self.child_type)

  @cached_property
  def snapshots(self):
    """List of all snapshots in the current block.

    The content of the given snapshots also contains the mapped audit field.
    """
    if not self.ids:
      return []
    snapshots = models.Snapshot.eager_query().filter(
        models.Snapshot.id.in_(self.ids)
    ).all()

    for snapshot in snapshots:  # add special snapshot attribute
      snapshot.revision.content["audit"] = {
          "type": "Audit",
          "id": snapshot.parent_id
      }
    return snapshots

  @cached_property
  def child_type(self):
    """Name of snapshot object types."""
    child_types = {snapshot.child_type for snapshot in self.snapshots}
    assert len(child_types) <= 1
    return child_types.pop() if child_types else ""

  @staticmethod
  def to_array():
    return [[]], [[]]  # header and body
