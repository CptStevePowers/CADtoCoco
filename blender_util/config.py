import json

class Config():
    def __init__(self,config_path):
        json_config = None
        with open(config_path, 'r') as j:
            json_config = json.load(j)

        self.input_dir = json_config['input_dir']
        self.output_dir = json_config['output_dir']

        components = json_config['components']
        self.components = {}
        for component in components:
            self.components[component] = components[component]