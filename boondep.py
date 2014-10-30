__all__ = ["Node"]
class Node(object):
  def __init__(self):
    self.dependencies = []
  def build(self):
    if self.needs_action():
      print("build: " + repr(self))
      return True
    return False
  def needs_action(self):
    raise NotImplementedError()

