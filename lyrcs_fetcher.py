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

from funasr.utils.time_util import secendToHMS, secendToLyc

# uwsgi --ini start.ini
# conda install uwsgi -c conda-forge  

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"mp3", "wav"}

model = AutoModel(
        model="paraformer-zh", model_revision="v2.0.4",
        vad_model="fsmn-vad", vad_model_revision="v2.0.4",
        punc_model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    return "hello fetch_lyrcs"

@app.route('/fetch_lyrcs', methods=['GET', 'POST'])
def fetch_lyrcs():
    
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
    return fetch_file_lyric_impl(savePath)
    
@app.route('/fetch_file_lyrcs', methods=['GET', 'POST'])
def fetch_file_lyrcs():
    path = request.args.get("path")
    
    if path is None:
        return jsonify({'error': 'No file part'})
    
    
    print("path:", path)
    return fetch_file_lyric_impl(path)
    
    
    
def fetch_file_lyric_impl(savePath, timeStapm=True):
    res = model.generate(input=savePath,
                     sentence_timestamp=timeStapm, 
            batch_size_s=300)
    
    # print(f"result:{res}")
    
    
    
    
    textLen = len(res[0]["text"])
    stampLen = len(res[0]["timestamp"])
    
    sentence_info = res[0]["sentence_info"]
    
    lyrcs = []
    for item in sentence_info:
        info = {}
        
        info["text"] = item["text"]
        info["start"] = "[" + secendToLyc(item["start"]) + "]"
        info["end"] = "[" + secendToLyc(item["end"]) + "]"
        info["end"] = "[" + secendToLyc(item["end"] ) + "]"
        
        lyrcs.append(info)
        
    print("res=====lyrcs:", lyrcs)

    try:
        return lyrcs
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e), "data":""})
    

if __name__ == "__main__":
    app.run(port=50000, host='0.0.0.0')
    
    # time_local = time.localtime(13590/1000)

    # dt = time.strftime("%H:%M:%S", time_local)
    
    # m, s = divmod(13590/1000, 60)
    # h, m = divmod(m, 60)
    # hms = "%02d:%02d:%02d" % (h, m, s)
    # hms = secendToHMS(13590/1000)
    # print("=====", hms)

