import requests
import os
import re
import json

class ModelUploader:
    filesArray = []
    metaDataFileID = 1

    def __init__(self, username="dharani@gmail.com", path=""):

        self.username = username
        self.path = path

    def UploadModel(self):
        files = os.listdir(self.path)

        for image in files:
            res = self.UploadFile(self.path + '/' + image)
            if 'file_uploaded' in res.keys():
                ModelUploader.filesArray.append(res['file_id'])
            if re.search('_metadata.txt', image):
                ModelUploader.metaDataFileID = res['file_id']

        self.metaDataExtraction()

    def UploadFile(self,file_path):
        filename = os.path.basename(file_path)
        multipart_form_data = {
            'file': (filename, open(file_path, 'rb'))
        }
        response = requests.post('http://localhost:4000/uploadToMongo/files', files=multipart_form_data)
        return response.json()

    def metaDataExtraction(self):
        metaInfo = {
            'file_id': ModelUploader.metaDataFileID,
            'Author': self.username,
            'categoryID': 'Image Classification',
            'model_name': 'test',
            'experiment': 'test1'
        }
        print(metaInfo)
        data = {
            'userId': self.username,
            'categoryId': 'Image Classification',
            'name': 'test',
            'experiment': 'test1',
            'metaInfo': metaInfo,
            'fileReferenceIDs': ModelUploader.filesArray
        }
        print(data)
        response = requests.post('http://localhost:4000/uploadToMongo/models', json=data)
        print(response)



# ob = ModelUploader("pavankotas@gmail.com","model")
# ob.UploadModel();
