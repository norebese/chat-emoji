import requests
import base64
import io
import os
from PIL import Image
from typing import List, Tuple

# 현재 스크립트 파일의 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# 프로젝트 루트 디렉토리 (server 폴더의 부모 디렉토리)
project_root = os.path.dirname(os.path.dirname(current_dir))

# default.png 파일의 경로
default_image_path = os.path.join(project_root, "server", "img", "default.png")


def generate_image(url: str, emotions: List[Tuple[str, float]], input_image_base64: str = None) -> str:
    # 감정을 문자열로 변환
    emotion_str = ', '.join([f"({emotion}:{score:.2f})" for emotion, score in emotions])

    # 입력 이미지 처리
    if input_image_base64:
        init_images = [input_image_base64]
    else:
        with open(default_image_path, "rb") as image_file:
            init_images = [base64.b64encode(image_file.read()).decode("utf-8")]

    payload = {
        "init_images": init_images,
        "prompt": f"(animation:1.2),best quality, (clean_background, white_background ),(close-up face shot:1.3), Character,emotion, {emotion_str}",
        "negative_prompt": "nsfw, worst quality, low quality, lowres, text, legwear",
        "steps": 28,
        "sampler_name": "DPM++ 2M SDE",
        "scheduler": "Karras",
        "denoising_strength": 0.6,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "batch_size": 1,
        "n_iter": 1,
        "seed": -1,
        "override_settings": {
            "sd_model_checkpoint": "dreamshaper_8.safetensors",
            "CLIP_stop_at_last_layers": 2,
        },
        "resize_mode": 1,  # 1은 "Crop and resize" 모드입니다
        "do_not_save_samples": True,
        "do_not_save_grid": True
    }

    try:
        response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
        response.raise_for_status()

        r = response.json()
        image_base64 = r['images'][0]
        return image_base64
    except requests.RequestException as e:
        print(f"Error generating image: {e}")
        return None


# 테스트 함수
def test_generate_image():
    # WebUI API 서버 URL
    url = "http://localhost:17860"  # 실제 URL로 변경해야 합니다

    # 테스트용 감정 데이터
    # emotions = [("happy", 0.8), ("excited", 0.6)]
    emotions = [('Tired/Instructive', 0.63), ('Irritable', 0.57), ('Complain/Complaint', 0.56)]

    # 이미지 생성
    generated_image_base64 = generate_image(url, emotions)

    if generated_image_base64:
        # base64 문자열을 이미지로 변환
        image_data = base64.b64decode(generated_image_base64)
        image = Image.open(io.BytesIO(image_data))

        # 이미지를 파일로 저장
        image.save("testimg.png")
        print("Image saved as testimg.png")
    else:
        print("Failed to generate image")


if __name__ == "__main__":
    test_generate_image()