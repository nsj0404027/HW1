import os
from PIL import Image

class FaceRecommender:
    def __init__(self):
        # 지원하는 연예인 목록 (샘플)
        self.celebrities = [
            '차은우', '장원영', '카리나', '박보검', '아이유', 
            '공유', '수지', '손석구', '한소희', '김수현'
        ]

    def recommend(self, image_path: str) -> str:
        """
        가벼운 오프라인용 모델을 대체합니다. 
        실제 딥러닝 모델 사용시 의존성(TF, PyTorch)이 무거워지므로, 
        이미지의 특징(가운데 픽셀 색상 및 크기 등)을 토대로 해싱하여 결정론적 결과를 반환합니다.
        """
        try:
            with Image.open(image_path) as img:
                img = img.convert('RGB')
                w, h = img.size
                center_pixel = img.getpixel((w // 2, h // 2))
                
                # 기초적인 해싱값을 사용하여 인덱스 추출 (이미지마다 동일한 결과 보장)
                hash_val = sum(center_pixel) + w + h
                idx = hash_val % len(self.celebrities)
                
                return self.celebrities[idx]
        except Exception:
            # 처리 중 예외 발생 시 기본값 반환
            return self.celebrities[0]
