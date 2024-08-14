import os

from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

from concurrent.futures import thread
from flask import jsonify
import os
from flask import Flask, request
import zipfile
import json
import base64
import shutil
import time
from werkzeug.utils import secure_filename


app = Flask(__name__)

ALLOWED_EXTENSIONS = {"mp3", "wav"}

model = AutoModel(
        model="paraformer-zh", model_revision="v2.0.4",
        vad_model="fsmn-vad", vad_model_revision="v2.0.4",
        punc_model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch"
    )

@app.route('/fetch_lyric', methods=['GET', 'POST'])
def fetch_lyric():
    
    file = request.files['file']
    
    if file is None:
        return jsonify({'error': 'No file part'})
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    print("filename:", file.filename)
    fileNameSplit = os.path.splitext(file.filename)
    
    fileExtension = fileNameSplit[-1][1:]
    if fileExtension not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Invalid file type'})
    
    secureName = secure_filename(str(file.filename))
    # print("secureName:", secureName)
    
    savePath = os.path.join('./temp_file', secureName)
    file.save(savePath)

# filepath = f"{model.model_path}/example/asr_example.wav"
    res = model.generate(input=savePath,
                     sentence_timestamp=True, 
            batch_size_s=300)
    
    sentence_info = res[0]["sentence_info"]
    print("res=====", res[0]["text"])
    
    try:
        return sentence_info
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})
    

if __name__ == "__main__":
    app.run(port=50000, host='0.0.0.0')

