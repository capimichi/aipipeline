import json

import requests

from aipipeline.task.BaseTask import BaseTask


class GenerateFileNameTask(BaseTask):
    content = None
    file_name = None

    def get_required_inputs(self):
        return ['content']

    def set_inputs(self, inputs):
        self.content = inputs['content']

    def run(self):
        llm_url = 'http://172.18.0.1:8000/v1'
        url = f'{llm_url}/chat/completions'
        response = requests.post(
            url=url,
            data=json.dumps({
                "model": "openhermes:v2.5",
                "messages": [
                    {"role": "user", "content": self.content}
                ]
            })
        )
        response_data = response.json()
        response = response_data['choices'][0]['message']['content']
        self.file_name = response

    def get_outputs(self):
        return {'file_name': self.file_name}
