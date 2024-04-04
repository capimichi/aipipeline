import yaml

from aipipeline.model.Pipeline import Pipeline
from aipipeline.model.Task import Task
from aipipeline.parser.TaskParser import TaskParser

class PipelineParser:
    """
    Class for parsing and running AI pipelines.
    """

    task_parser: TaskParser = None

    def __init__(self, task_parser: TaskParser):
        """
        Initialize PipelineParser with a TaskParser instance.

        :param task_parser: TaskParser instance
        """
        self.task_parser = task_parser

    def run(self, pipeline: Pipeline):
        """
        Run the given pipeline.

        :param pipeline: Pipeline instance
        """
        tasks = pipeline.tasks

        # Loop through tasks until all are processed
        while len(tasks) > 0:

            # Get the first task and remove it from the list
            current_task: Task = tasks.pop(0)

            task_instances = []
            if(current_task.is_multiple()):
                for i in range(0, 100):
                    if(self.task_parser.has_task_instance(current_task, i)):
                        task_instances.append(self.task_parser.get_task_instance(current_task, i))
            else:
                task_instances.append(self.task_parser.get_task_instance(current_task))

            for task_instance in task_instances:
                # Get the task instance from the task parser
                # task_instance = self.task_parser.get_task_instance(current_task)
                # If the task has inputs, set them in the task instance
                if (current_task.get_inputs()):
                    task_instance.set_inputs(current_task.get_inputs())

                print(f"Running task {current_task.id}")
                print(f"Inputs: {current_task.get_inputs()}")
                # Run the task instance
                task_instance.run()
                print(f"Outputs: {task_instance.get_outputs()}")

                # If the task has outputs, process them
                outputs = current_task.get_outputs()
                if (outputs):
                    output_values = task_instance.get_outputs()
                    for output_field in outputs:
                        output_value = output_values[output_field]

                        output_destination = outputs[output_field]
                        # If the output destination is not a list, make it a list
                        if(not isinstance(output_destination, list)):
                            output_destinations = [output_destination]
                        else:
                            output_destinations = output_destination

                        # Loop through output destinations and set the output value in the corresponding task
                        for output_destination in output_destinations:
                            output_task_id = self.task_parser.get_output_task_id(output_destination)
                            output_input = self.task_parser.get_output_input(output_destination)
                            for loop_task in tasks:
                                if loop_task.id == output_task_id:
                                    if(loop_task.is_multiple()):
                                        if(isinstance(output_value, list)):
                                            index = 0
                                            for output_value_single in output_value:
                                                self.task_parser.get_task_instance(loop_task, index).set_inputs({output_input: output_value_single})
                                                index += 1
                                        else:
                                            for i in range(0, 100):
                                                self.task_parser.get_task_instance(loop_task, i).set_inputs({output_input: output_value})
                                    else:
                                        self.task_parser.get_task_instance(loop_task).set_inputs({output_input: output_value})

    def parse(self, pipeline_path):
        """
        Parse a pipeline from a YAML file.

        :param pipeline_path: Path to the pipeline YAML file
        :return: Pipeline instance
        """
        with open(pipeline_path, 'r') as stream:
            pipeline_data = yaml.safe_load(stream)

        # Validate the pipeline data and create a Pipeline instance
        pipeline = Pipeline.model_validate(pipeline_data)
        self.validate(pipeline)
        return pipeline

    def validate(self, pipeline : Pipeline):
        """
        Validate a pipeline.

        :param pipeline: Pipeline instance
        """
        tasks = pipeline.tasks
        # Validate each task in the pipeline
        for task in tasks:
            self.task_parser.validate(task, pipeline)