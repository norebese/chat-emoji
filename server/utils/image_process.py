import requests
import base64
import io
from PIL import Image
from typing import List, Tuple


def generate_image(url: str, emotions: List[Tuple[str, float]]) -> str:
    # 감정을 문자열로 변환
    emotion_str = ', '.join([f"({emotion}:{score:.2f})" for emotion, score in emotions])

    payload = {
        "prompt": f"(animation:1.2),best quality, (clean_background, white_background ),(close-up face shot:1.3), Character,emotion, {emotion_str}",
        "negative_prompt": "nsfw, worst quality, low quality, lowres, text, legwear",
        "steps": 28,
        "sampler_name": "DPM++ 2M SDE",
        "scheduler": "Karras",
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
                        "image": "defaultpose_data.png",
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

    try:
        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
        response.raise_for_status()  # 오류 상태 코드에 대해 예외를 발생시킵니다.

        r = response.json()
        image_base64 = r['images'][0]
        return image_base64
    except requests.RequestException as e:
        print(f"Error generating image: {e}")
        return None