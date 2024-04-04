import yaml

from aipipeline.model.Pipeline import Pipeline
from aipipeline.model.Task import Task
import importlib

class TaskParser:

    instances = {}

    def validate(self, task : Task, pipeline : Pipeline):
        task_instance = self.get_task_instance(task)

        self.has_required_inputs(task_instance, task, pipeline)


    def has_task_instance(self, task : Task, index = None):
        task_id = task.id
        if(index != None):
            task_id = task_id + str(index)
        return task_id in self.instances

    def get_task_instance(self, task : Task, index = None):
        task_id = task.id
        if(index != None):
            task_id = task_id + str(index)
        task_class = task.type
        if not task_id in self.instances:
            task_class = getattr(importlib.import_module("aipipeline.task." + task_class), task_class)
            instance = task_class()
            self.instances[task_id] = instance
        return self.instances[task_id]

    def has_required_inputs(self, task_instance, task: Task, pipeline : Pipeline):
        required_inputs = task_instance.get_required_inputs()
        existing_inputs = []
        inputs = task.get_inputs()

        for required_input in required_inputs:
            if required_input in inputs:
                existing_inputs.append(required_input)

        task_id = task.id
        missing_inputs = list(set(required_inputs) - set(existing_inputs))
        for missing_input in missing_inputs:
            loop_tasks = pipeline.tasks
            for loop_task in loop_tasks:
                loop_outputs = loop_task.get_outputs()
                for output_key in loop_outputs:
                    output = loop_outputs[output_key]
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

        missing_inputs = list(set(required_inputs) - set(existing_inputs))

        if(len(existing_inputs) != len(required_inputs)):
            raise Exception(f"Task {task_instance} is missing required inputs {missing_inputs}")

    def get_output_task_id(self, output: str):
        return output.split('.')[0]

    def get_output_input(self, output: str):
        return output.split('.')[1]
        


