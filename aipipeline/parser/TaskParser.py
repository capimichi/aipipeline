import yaml

from aipipeline.model.Pipeline import Pipeline
from aipipeline.model.Task import Task
import importlib

class TaskParser:

    instances = {}

    def validate(self, task : Task, pipeline : Pipeline):
        task_instance = self.get_task_instance(task)

        self.has_required_inputs(task_instance, task)


    def get_task_instance(self, task : Task):
        task_class = task.type
        if not task_class in self.instances:
            task_class = getattr(importlib.import_module("aipipeline.task." + task_class), task_class)
            instance = task_class()
            self.instances[task_class] = instance
        return self.instances[task_class]

    def has_required_inputs(self, task_instance, task: Task):
        required_inputs = task_instance.get_required_inputs()
        existing_inputs = []
        inputs = task.inputs

        for required_input in required_inputs:
            if required_input in inputs:
                existing_inputs.append(required_input)

        task_id = task.id
        outputs = task.outputs
        missing_inputs = list(set(required_inputs) - set(existing_inputs))
        for missing_input in missing_inputs:
            for output_key in outputs:
                output = outputs[output_key]
                output_list = []
                if not isinstance(output, list):
                    output_list.append(output)
                else:
                    output_list = output

                for output in output_list:
                    output_task_id = self.get_output_task_id(output)
                    output_input = self.get_output_input(output)
                    if output_task_id == task_id and output_input == missing_input:
                        existing_inputs.append(missing_input)

        if(len(existing_inputs) != len(required_inputs)):
            raise Exception(f"Task {task_instance} is missing required inputs {required_inputs}")

    def get_output_task_id(self, output: str):
        return output.split('.')[0]

    def get_output_input(self, output: str):
        return output.split('.')[1]
        


