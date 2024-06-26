import json

import requests

from aipipeline.task.BaseTask import BaseTask


class AskAi(BaseTask):
    prompt = None
    argument1 = None
    argument2 = None

    response = None

    def get_required_inputs(self):
        return ['prompt']

    def set_inputs(self, inputs):
        if('prompt' in inputs):
            self.prompt = inputs['prompt']
        if('argument1' in inputs):
            self.argument1 = inputs['argument1']
        if('argument2' in inputs):
            self.argument2 = inputs['argument2']

    def run(self):

        final_prompt = self.prompt

        is_array = False

        if(self.argument1 != None):
            argument1 = self.argument1
            final_prompt = final_prompt.replace('{{argument1}}', argument1)

        if(self.argument2 != None):
            argument2 = self.argument2
            final_prompt = final_prompt.replace('{{argument2}}', argument2)

        # llm_url = 'http://172.18.0.1:8000/v1'
        llm_url = 'http://0.0.0.0:4000/v1'
        url = f'{llm_url}/chat/completions'
        response = requests.post(
            url=url,
            data=json.dumps({
                "model": "openhermes:v2.5",
                "messages": [
                    {"role": "user", "content": final_prompt}
                ]
            })
        )
        response_data = response.json()
        response = response_data['choices'][0]['message']['content']

        self.response = response

    def get_outputs(self):
        return {'response': self.response}
