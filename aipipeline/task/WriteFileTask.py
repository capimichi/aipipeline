from aipipeline.task.BaseTask import BaseTask


class WriteFileTask(BaseTask):
    file_path = None
    file_content = None

    def add_params(self, params):
        self.file_path = params['file_path']
        self.file_content = params['file_content']

    def run(self):
        with open(self.file_path, 'w') as file:
            file.write(self.file_content)

    def get_outputs(self):
        return {'file_path': self.file_path}
