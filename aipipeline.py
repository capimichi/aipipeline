import sys
import os
import yaml
import requests
import re
import subprocess

from aipipeline.parser.PipelineParser import PipelineParser

pipeline_path = sys.argv[1]

pipeline_parser = PipelineParser()

pipeline = pipeline_parser.parse(pipeline_path)
