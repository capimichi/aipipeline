import os

from aipipeline.parser.PipelineParser import PipelineParser
from aipipeline.parser.TaskParser import TaskParser


class DefaultContainer:

    instance = None
    classes = {}

    @staticmethod
    def get_instance():
        if DefaultContainer.instance is None:
            DefaultContainer.instance = DefaultContainer()
        return DefaultContainer.instance

    def __init__(self):

        self.set(TaskParser.__name__, TaskParser())
        self.set(PipelineParser.__name__, PipelineParser(
            self.get(TaskParser.__name__)
        ))



    def get(self, class_name):
        return self.classes[class_name]

    def set(self, class_name, instance):
        self.classes[class_name] = instance
