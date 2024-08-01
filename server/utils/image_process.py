import requests
import base64
import io
from PIL import Image

# WebUI의 주소와 포트를 적절히 수정하세요
url = "http://sooserver.duckdns.org:17860"

payload = {
    "prompt": "(animation:1.2),best quality, (clean_background, white_background ),(close-up face shot:1.3), Character,emotion, (Annoyed:0.86), (Complain:0.78), (Difficult:0.71)",
    "negative_prompt": "nsfw, worst quality, low quality, lowres, text, legwear",
    "steps": 28,
    "sampler_name": "DPM++ 2M SDE",  # 대문자 그대로 유지
    "scheduler": "Karras",  # 'K'를 대문자로 변경
    "cfg_scale": 7,
    "width": 1024,
    "height": 1024,
    "batch_size": 1,
    "n_iter": 1,
    "seed": -1,
    "override_settings": {
        "sd_model_checkpoint": "sd_xl_base_1.0.safetensors",
        "CLIP_stop_at_last_layers": 2,
    },
    "alwayson_scripts": {
        "controlnet": {
            "args": [
                {
                    "image": "defaultpose_data.png",  # 'input_image'를 'image'로 변경
                    "module": "openpose",
                    "model": "controlnet++_union_sdxl.safetensors",
                    "weight": 1.0,
                    "resize_mode": "Just Resize",
                    "processor_res": 1024,
                    "threshold_a": 0.5,
                    "threshold_b": 0.5,
                    "guidance_start": 0.0,
                    "guidance_end": 1.0,
                    "control_mode": "My prompt is more important",
                    "pixel_perfect": False
                }
            ]
        }
    }
}


def generate_image():
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    if response.status_code == 200:
        r = response.json()
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
        image.save('output.png')
        print("Image generated and saved as output.png")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    generate_image()