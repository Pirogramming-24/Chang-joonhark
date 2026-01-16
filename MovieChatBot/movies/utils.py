import requests
from django.conf import settings
from .models import Movie

def fetch_and_save_movies(total_pages=5):  
    api_key = settings.TMDB_API_KEY
    base_url = "https://api.themoviedb.org/3"
    
    print(f"🎬 영화 데이터 {total_pages}페이지 수집 시작...")

    # [수정 1] 1페이지부터 설정한 페이지까지 반복
    for page in range(1, total_pages + 1):
        print(f"  📄 {page} 페이지 가져오는 중...")
        
        # [수정 2] URL 뒤에 &page={page} 추가
        url = f"{base_url}/movie/popular?api_key={api_key}&language=ko-KR&page={page}"
        response = requests.get(url)
        
        if response.status_code != 200:
            continue

        movies_data = response.json().get('results', [])

        for item in movies_data:
            # 이미 저장된 영화는 패스 (중복 방지)
            if Movie.objects.filter(tmdb_id=item['id']).exists():
                continue

            # 상세 정보 가져오기 (감독, 배우 등)
            detail_url = f"{base_url}/movie/{item['id']}?api_key={api_key}&language=ko-KR&append_to_response=credits"
            detail_res = requests.get(detail_url)
            
            if detail_res.status_code == 200:
                detail_data = detail_res.json()
                
                # 감독, 배우, 장르 등 데이터 정리
                director = "알 수 없음"
                crews = detail_data.get('credits', {}).get('crew', [])
                for crew in crews:
                    if crew['job'] == 'Director':
                        director = crew['name']
                        break
                
                cast_list = detail_data.get('credits', {}).get('cast', [])[:3]
                actors = ", ".join([actor['name'] for actor in cast_list])
                
                genres_list = detail_data.get('genres', [])
                genre = ", ".join([g['name'] for g in genres_list])

                poster_path = item.get('poster_path')
                full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

                # DB 저장
                Movie.objects.create(
                    tmdb_id=item['id'],
                    title=item['title'],
                    release_date=item.get('release_date') or None,
                    genre=genre,
                    director=director,
                    actors=actors,
                    runtime=detail_data.get('runtime'),
                    poster_path=full_poster_url,
                    overview=item.get('overview', ''),
                    # 평점이나 영어 줄거리 로직은 뺐습니다.
                    is_tmdb=True
                )
                print(f"    ✅ 저장: {item['title']}")

    print("수집 끝!")