from aipipeline.task.BaseTask import BaseTask


class SplitListTask(BaseTask):

    content = None
    results = None

    def get_required_inputs(self):
        return ['content']

    def set_inputs(self, inputs):
        if('content' in inputs):
            self.content = inputs['content']

    def run(self):
        first_results = self.content.split("\n")
        results = []
        for result in first_results:
            result = result.strip()
            if(not result.endswith(':')):

                if(result.startswith('-')):
                    result = result[1:]

                if(result.startswith('*')):
                    result = result[1:]

                for i in range(0, 20):
                    if(result.startswith(f'{i}.')):
                        result = result[2:]

                result = result.strip()
                results.append(result)

        self.results = results


    def get_outputs(self):
        return {'results': self.results}