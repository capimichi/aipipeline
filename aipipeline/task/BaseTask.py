from abc import abstractmethod


class BaseTask():

    def get_required_inputs(self):
        return []

    def set_inputs(self, inputs):
        pass

    def get_outputs(self):
        pass

    @abstractmethod
    def run(self):
        pass
