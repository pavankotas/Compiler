import requests
# from FileUploader import ModelUploader
# experiment = {'project_name': 'LSTM',
#               'project_id': 'LSTM_061819-143828_c35c614a-1a80-4bef-9104-6c6aa26418d4',
#               'experiment_id': 'LSTM_061819-143828_c35c614a-1a80-4bef-9104-6c6aa26418d4',
#               'user_name': 'Sirisha Rella',
#               'epochs': ' 3',
#               'batch_size': ' 32',
#               'input_shape': (None, 152),
#               'layers_count': 4,
#               'output_shape': (None, 2),
#               'Optimizer': 'Adam',
#               'LossFunction': 'categorical_crossentropy',
#               'callbacks_log': 'C:/Users/pavan/AppData/Local/Programs/Python/Python36/Lib/site-packages/training.log', 'model_file': 'C:/Users/pavan/AppData/Local/Programs/Python/Python36/Lib/site-packages\\weights-improvement-03-0.99.hdf5',
#               'predict_function': 'C:/Users/pavan/AppData/Local/Programs/Python/Python36/Lib/site-packages/auto_predict.py'}
#
# uploader = ModelUploader()
#
#
# def saveToLocalDB(expData):
#     uploadFiles(expData)
#     files = ['callbacks_log', 'model_file', 'predict_function']
#     data = {}
#     for key in expData.keys():
#         if key not in files:
#                 data[key] = expData[key]
#
#     data['fileIDs'] = uploader.filesArray
#     print(data)
#     response = requests.post('http://localhost:4000/kerasfitparameters', json=data)
#     print(response)
#
#
# def uploadFiles(expData):
#     files = ['callbacks_log', 'model_file', 'predict_function']
#     for key in expData.keys():
#         if key in files:
#             res = uploader.UploadFile(expData['callbacks_log'])
#             if 'file_uploaded' in res.keys():
#                 uploader.filesArray.append(res['file_id'])
#
#
# saveToLocalDB(experiment)
def saveToRemote(experiment_id):
    res = requests.get('http://localhost:4000/kerasfitparameters/getParams/' + experiment_id)
    if res.status_code == 200:
        print("Your experiment has been pushed to public repository")
