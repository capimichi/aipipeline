import yaml

from aipipeline.model.Pipeline import Pipeline
from aipipeline.parser.TaskParser import TaskParser


class PipelineParser:

    task_parser: TaskParser = None

    def __init__(self, task_parser: TaskParser):
        self.task_parser = task_parser

    def run(self, pipeline: Pipeline):
        tasks = pipeline.tasks
        for task in tasks:
            self.task_parser.run(task, pipeline)

    def parse(self, pipeline_path):
        with open(pipeline_path, 'r') as stream:
            pipeline_data = yaml.safe_load(stream)

        pipeline = Pipeline.model_validate(pipeline_data)
        self.validate(pipeline)
        return pipeline

    def validate(self, pipeline : Pipeline):
        tasks = pipeline.tasks
        for task in tasks:
            self.task_parser.validate(task, pipeline)



