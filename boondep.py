__all__ = ["Node", "Graph"]
class Node(object):
  def __init__(self, dependencies=None):
    self.dependencies = []
    if dependencies != None:
      self.dependencies.extend(dependencies)
  def ensure_built(self):
    children_needed_updates = [dependency.ensure_built() for dependency in self.dependencies]
    if self.needs_action(children_needed_updates):
      self.build()
      return True
    return False
  def __hash__(self):
    return id(self)
  def build(self):
    raise NotImplementedError()
  def needs_action(self, children_needed_updates):
    raise NotImplementedError()

class Graph(object):
  def __init__(self, *roots):
    self.nodes = []
    visited_nodes = set()
    def recurse(node):
      if node in visited_nodes:
        return
      visited_nodes.add(node)
      self.nodes.append(node)
      for child in node.dependencies:
        recurse(child)
    for root in roots:
      recurse(root)
  def __str__(self):
    lines = []
    for node in self.nodes:
      lines.append(repr(node) + ": " + repr(node.dependencies))
    return "\n".join(lines)
