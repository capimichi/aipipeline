import sys
import os
import yaml
import requests
import re
import subprocess

from aipipeline.container.DefaultContainer import DefaultContainer
from aipipeline.parser.PipelineParser import PipelineParser

pipeline_path = sys.argv[1]

default_container = DefaultContainer.get_instance()

pipeline_parser:PipelineParser = default_container.get(PipelineParser.__name__)

pipeline = pipeline_parser.parse(pipeline_path)
