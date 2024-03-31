import yaml

from aipipeline.model.Pipeline import Pipeline
from aipipeline.parser.TaskParser import TaskParser


class PipelineParser:

    task_parser: TaskParser = None

    def __init__(self, task_parser: TaskParser):
        self.task_parser = task_parser

    def run(self, pipeline: Pipeline):
        tasks = pipeline.tasks

        current_task = None
        while len(tasks) > 0:
            if not current_task:
                current_task = tasks.pop(0)

            task_instance = self.task_parser.get_task_instance(current_task)
            if (current_task.get_inputs()):
                task_instance.set_inputs(current_task.get_inputs())

            task_instance.run()

            outputs = current_task.get_outputs()
            if (not outputs):
                current_task = None
            else:
                output_values = task_instance.get_outputs()
                for output_field in outputs:
                    output_value = output_values[output_field]

                    # find destination for this value
                    output_destinations = []
                    output_destination = outputs[output_field]
                    if(not isinstance(output_destination, list)):
                        output_destinations = [output_destination]
                    else:
                        output_destinations = output_destination

                    for output_destination in output_destinations:
                        output_task_id = self.task_parser.get_output_task_id(output_destination)
                        output_input = self.task_parser.get_output_input(output_destination)
                        for loop_task in tasks:
                            if loop_task.id == output_task_id:
                                self.task_parser.get_task_instance(loop_task).set_inputs({output_input: output_value})
                                tasks.remove(loop_task)
                                current_task = loop_task
                                break



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



