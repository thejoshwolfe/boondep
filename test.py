#!/usr/bin/env python
import boondep
import os

class GeneratedFile(boondep.Node):
  def __init__(self, path, *args, **kwargs):
    super(GeneratedFile, self).__init__(*args, **kwargs)
    self.path = path
  def __repr__(self):
    return "GeneratedFile({})".format(repr(self.path))
  def needs_action(self, children_needed_updates):
    if any(children_needed_updates):
      return True
    return not os.path.isfile(self.path)
  def build(self):
    print("build: " + repr(self))

class SourceFile(boondep.Node):
  def __init__(self, path):
    super(SourceFile, self).__init__()
    self.path = path
  def __repr__(self):
    return "SourceFile({})".format(repr(self.path))
  def needs_action(self, children_needed_updates):
    return False

util_h = SourceFile("util.h")
util_c = SourceFile("util.c")
main_c = SourceFile("main.c")

util_o = GeneratedFile("util.o", dependencies=[util_c, util_h])
main_o = GeneratedFile("main.o", dependencies=[main_c, util_h])
binary = GeneratedFile("foo", dependencies=[util_o, main_o])

graph = boondep.Graph(binary)

traversal = graph.traversal()
while True:
  ready_nodes = traversal.drain_ready_nodes()
  if ready_nodes == None:
    break
  print("")
  for node in ready_nodes:
    print(node)
    traversal.done_with_node(node)
