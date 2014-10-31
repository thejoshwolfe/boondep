__all__ = ["Node"]
class Node(object):
  def __init__(self):
    self.dependencies = []
  def ensure_built(self):
    children_needed_updates = [dependency.ensure_built() for dependency in self.dependencies]
    if self.needs_action(children_needed_updates):
      self.build()
      return True
    return False
  def build(self):
    raise NotImplementedError()
  def needs_action(self, children_needed_updates):
    raise NotImplementedError()
