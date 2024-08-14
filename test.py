import os
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

model_dir = "iic/SenseVoiceSmall"

filepath = os.path.join("./", "vocals.mp3")

model = AutoModel(
    model="paraformer-zh", model_revision="v2.0.4",
    vad_model="fsmn-vad", vad_model_revision="v2.0.4",
    punc_model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch"
)

# filepath = f"{model.model_path}/example/asr_example.wav"
res = model.generate(input=filepath,
                     sentence_timestamp=True, 
            batch_size_s=300)
text = rich_transcription_postprocess(res[0]["text"])
timestamp = res[0]["timestamp"]
text = res[0]["text"]

print("res=====", res[0]["sentence_info"])
