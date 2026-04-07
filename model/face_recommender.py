import os
from PIL import Image

class FaceRecommender:
    def __init__(self):
        # 지원하는 연예인 목록 (배우/가수 분류)
        self.celebrities = {
            'actor': ['공유', '박보검', '손석구', '한소희', '김수현'],
            'singer': ['차은우', '장원영', '카리나', '아이유', '수지']
        }
        
        # 전체 리스트 
        self.all_celebrities = self.celebrities['actor'] + self.celebrities['singer']
        
        # 소셜 미디어 및 나무위키 주소 데이터베이스
        self.social_links = {
           '차은우': {'instagram': 'https://www.instagram.com/eunwo.o_c/', 'namuwiki': 'https://namu.wiki/w/%EC%B0%A8%EC%9D%80%EC%9A%B0'},
           '장원영': {'instagram': 'https://www.instagram.com/for_everyoung10/', 'namuwiki': 'https://namu.wiki/w/%EC%9E%A5%EC%9B%90%EC%98%81'},
           '카리나': {'instagram': 'https://www.instagram.com/katarinabluu/', 'namuwiki': 'https://namu.wiki/w/%EC%B9%B4%EB%A6%AC%EB%82%98(aespa)'},
           '박보검': {'instagram': 'https://www.instagram.com/bogummy/', 'namuwiki': 'https://namu.wiki/w/%EB%B0%95%EB%B3%B4%EA%B2%80'},
           '아이유': {'instagram': 'https://www.instagram.com/dlwlrma/', 'namuwiki': 'https://namu.wiki/w/%EC%95%84%EC%9D%B4%EC%9C%A0'},
           '공유': {'instagram': 'https://www.instagram.com/gongyoo_official/', 'namuwiki': 'https://namu.wiki/w/%EA%B3%B5%EC%9C%A0(%EB%B0%B0%EC%9A%B0)'},
           '수지': {'instagram': 'https://www.instagram.com/skuukzky/', 'namuwiki': 'https://namu.wiki/w/%EC%88%98%EC%A7%80(1994)'},
           '손석구': {'instagram': 'https://www.instagram.com/sonsukku/', 'namuwiki': 'https://namu.wiki/w/%EC%86%90%EC%84%9D%EA%B5%AC'},
           '한소희': {'instagram': 'https://www.instagram.com/xeesoxee/', 'namuwiki': 'https://namu.wiki/w/%ED%95%9C%EC%86%8C%ED%9D%AC'},
           '김수현': {'instagram': 'https://www.instagram.com/soohyun_k216/', 'namuwiki': 'https://namu.wiki/w/%EA%B9%80%EC%88%98%ED%98%84(1988)'}
       }

    def recommend(self, image_path: str, category: str = "all") -> dict:
        """
        카테고리 필터링을 지원하는 오프라인 오버레이 모델.
        """
        # 필터링 로직
        target_list = self.all_celebrities
        if category == "actor":
            target_list = self.celebrities['actor']
        elif category == "singer":
            target_list = self.celebrities['singer']

        try:
            with Image.open(image_path) as img:
                img = img.convert('RGB')
                w, h = img.size
                center_pixel = img.getpixel((w // 2, h // 2))
                
                # 기초적인 해싱값을 사용하여 인덱스 추출 (이미지마다 동일한 결과 보장)
                hash_val = sum(center_pixel) + w + h
                idx = hash_val % len(target_list)
                name = target_list[idx]
        except Exception:
            # 처리 중 예외 발생 시 기본값 반환
            name = target_list[0]
            
        return {
            "name": name,
            "instagram": self.social_links[name]["instagram"],
            "namuwiki": self.social_links[name]["namuwiki"]
        }
