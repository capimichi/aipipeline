from aipipeline.task.BaseTask import BaseTask


class ReadFileTask(BaseTask):

    file_path = None
    content = None

    def get_required_inputs(self):
        return ['file_path']

    def set_inputs(self, inputs):
        if('file_path' in inputs):
            self.file_path = inputs['file_path']

    def run(self):
        with open(self.file_path, 'r') as file:
            self.content = file.read()
        return self.content

    def get_outputs(self):
        return {'content': self.content}