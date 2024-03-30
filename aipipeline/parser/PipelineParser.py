import yaml

from aipipeline.model.Pipeline import Pipeline


class PipelineParser:
    def __init__(self):
        pass

    def parse(self, pipeline_path):
        with open(pipeline_path, 'r') as stream:
            pipeline_data = yaml.safe_load(stream)

        pipeline = Pipeline.model_validate(pipeline_data)

