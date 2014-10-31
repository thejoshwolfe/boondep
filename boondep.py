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
    node_to_dependency_closure = {}
    self.node_to_dependency_closure = node_to_dependency_closure
    def recurse(node):
      try: return self.node_to_dependency_closure[node]
      except KeyError: pass
      dependency_closure = set(node.dependencies)
      self.node_to_dependency_closure[node] = dependency_closure
      for child in node.dependencies:
        dependency_closure.update(recurse(child))
      if node in dependency_closure:
        raise Exception("circular dependency")
      return dependency_closure
    for root in roots:
      recurse(root)
    self.nodes = list(self.node_to_dependency_closure.keys())
    # TODO: why are we sorting anything?
    class ComparableWithDependencyCloser(object):
      def __init__(self, node):
        self.node = node
      def __lt__(self, other):
        return self.node in node_to_dependency_closure[other.node]
    self.nodes.sort(key=ComparableWithDependencyCloser)
  def traversal(self):
    graph = self
    class Traversal(object):
      def __init__(self):
        self.in_progress_nodes = set()
        self.done_nodes = set()
      def drain_ready_nodes(self):
        if len(self.done_nodes) == len(graph.nodes):
          return None
        ready_nodes = [
          node for node in graph.nodes
          if node not in self.in_progress_nodes
          and node not in self.done_nodes
          and graph.node_to_dependency_closure[node] <= self.done_nodes
        ]
        self.in_progress_nodes.update(ready_nodes)
        return ready_nodes
      def done_with_node(self, node):
        self.in_progress_nodes.remove(node)
        self.done_nodes.add(node)
    return Traversal()
  def __str__(self):
    lines = []
    for node in self.nodes:
      lines.append(repr(node) + ": " + repr(self.node_to_dependency_closure[node]))
    return "\n".join(lines)
