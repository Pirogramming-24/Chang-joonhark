import re

class NutrientParser:
    @staticmethod
    def parse(texts):
        data = {'calories': 0, 'carbohydrate': 0, 'protein': 0, 'fat': 0}
        
        full_text = " ".join(texts)
        full_text = full_text.replace(":", ".")
        full_text = full_text.replace("kca!", "kcal")
        full_text = full_text.replace("kca]", "kcal")
        full_text = full_text.replace("kca", "kcal")
        full_text = full_text.replace("'", " ")

        full_text = re.sub(r'(\d+)9(\d{1,2}%)', r'\1 \2', full_text)

        # [보조] 한글+숫자 분리 (단백질192 -> 단백질 192)
        full_text = re.sub(r'([가-힣])(\d)', r'\1 \2', full_text)
        
        # [보조] 일반 뭉침 분리 (혹시 9가 아닌 다른 숫자가 꼈을 때)
        full_text = re.sub(r'(\d+)(\d{1,2}%)', r'\1 \2', full_text)

        def get_value(keywords):
            for key in keywords:
                # (?!\s*mg) : 나트륨(mg)은 절대 가져오지 마라
                regex = f"{key}[^0-9]*?(\d+(?:\.\d+)?)(?!\s*mg)"
                match = re.search(regex, full_text)
                
                if match:
                    val = float(match.group(1))
                    
                    # [안전장치] 여전히 50이 넘고 끝자리가 9라면 자름 (389 -> 38)
                    # (위의 정규식으로 대부분 해결되지만, 공백이 있는 경우를 대비)
                    if val > 50 and int(val) % 10 == 9:
                        print(f"✂️ {key} 꼬리자르기: {val} -> {int(val)//10}")
                        val = int(val) // 10
                        
                    return val
            return 0

        def get_calories():
            matches = re.findall(r'(\d+(?:\.\d+)?)\s*kcal', full_text, re.IGNORECASE)
            valid = [float(x) for x in matches if float(x) < 5000 and float(x) != 2000]
            return max(valid) if valid else 0


        data['calories'] = int(get_calories())
        data['carbohydrate'] = get_value(['탄수화물', '탄'])
        data['protein'] = get_value(['단백질', '단'])
        data['fat'] = get_value(['지방', '류'])

        for k, v in data.items():
            if v % 1 == 0:
                data[k] = int(v)

        return data