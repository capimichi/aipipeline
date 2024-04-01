from aipipeline.task.BaseTask import BaseTask
import os

class WriteFileTask(BaseTask):
    path = None
    content = None

    def get_required_inputs(self):
        return ['path', 'content']

    def set_inputs(self, inputs):
        if('path' in inputs):
            self.path = inputs['path']
        if('content' in inputs):
            self.content = inputs['content']

    def run(self):
        # remove the double apex from the path
        self.path = self.path.replace('"', "")
        directory = os.path.dirname(self.path)
        if len(directory) > 0 and not os.path.exists(directory):
            os.makedirs(directory)
        with open(self.path, 'w') as file:
            file.write(self.content)

    def get_outputs(self):
        return {'path': self.path}
