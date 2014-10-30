#!/usr/bin/env python
import boondep
import os

class FileNode(boondep.Node):
  def __init__(self, path):
    super(FileNode, self).__init__()
    self.path = path
  def __repr__(self):
    return "FileNode({})".format(repr(self.path))
  def needs_action(self):
    if any(child.needs_action() for child in self.dependencies):
      return True
    return not os.path.isfile(self.path)

binary = FileNode("foo")
source = FileNode("main.c")
binary.dependencies.append(source)

binary.build()
