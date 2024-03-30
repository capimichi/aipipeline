import json

import requests

from aipipeline.task.BaseTask import BaseTask


class SummarizeTextTask(BaseTask):

    text = None
    summary = None

    def get_required_inputs(self):
        return ['text']

    def set_inputs(self, inputs):
        self.text = inputs['text']

    def run(self):
        llm_url = 'http://172.18.0.1:8000/v1'
        url = f'{llm_url}/chat/completions'
        response = requests.post(
            url=url,
            data=json.dumps({
                "model": "openhermes:v2.5",
                "messages": [
                    {"role": "user", "content": self.text}
                ]
            })
        )
        response_data = response.json()
        response = response_data['choices'][0]['message']['content']
        self.summary = response

    def get_outputs(self):
        return {'summary': self.summary}