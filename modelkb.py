import inspect
from Parser import AST
from datetime import datetime
from uuid import uuid4
import re
import requests

class Experiment:
    experiment_metadata = {}
    def __init__(self, title, user):
        self.title = title
        self.user = user
        self.experiment_metadata = dict()



    #For tracking experiment
    def track(self):

        self.experiment_metadata['experiment_name'] = self.title
        self.experiment_metadata['user_name'] = self.user
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        print(module)
        self.extract_hyperparameters('sample.py')

        # print(self.experiment_metadata)
        #Parameters that I'm expecting from AST
        # self.experiment_metadata['framework'] = 'keras'
        # self.experiment_metadata['size'] = '20'

        # for metadata in self.hyperparameters:
        #     self.experiment_metadata['epochs'] = metadata['epochs']
        #     self.experiment_metadata['batch_size'] = metadata['batch_size']
        #
        # for metadata in self.parameters:
        #     self.experiment_metadata['layers_count'] = metadata['layers_count']
        #     self.experiment_metadata['input_shape'] = metadata['input_shape']
        #     self.experiment_metadata['output_shape'] = metadata['output_shape']
        #     self.experiment_metadata['optimizer_function'] = metadata['optimizer_function']
        #     self.experiment_metadata['loss_function'] = metadata['loss_function']

    def extract_hyperparameters(self, filename):
        print(self.title)
        astObj = AST()
        print(filename)
        hyperParams = astObj.ParseAst(filename, self.title)
        print("Sirisha")
        print(hyperParams)
        self.saveToDB(hyperParams, self.title)


    def saveToDB(self, ls, projName):
        fitParams = '(x|y|batch_size|epochs|verbose|callbacks|validation_split|validation_data|shuffle|class_weight|' \
                    'sample_weight|initial_epoch|steps_per_epoch|validation_steps|validation_steps)'
        data = {}
        for ob in ls:
            ob = ob.split('=')
            if re.search(fitParams, ob[0].strip()):
                data[ob[0].strip()] = ob[1].strip()
        data['experimentID'] = '1000'
        data['projectName'] = projName
        print(data)
        response = requests.post('https://testmodelhubbackend.herokuapp.com/kerasfitparameters', json=data)












