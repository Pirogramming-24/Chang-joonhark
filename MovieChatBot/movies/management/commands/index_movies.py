from django.core.management.base import BaseCommand
from movies.models import Movie
from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma
from django.conf import settings
import os

class Command(BaseCommand):
    help = '영화 데이터를 벡터로 변환하여 ChromaDB에 저장합니다.'

    def handle(self, *args, **options):
        # 1. DB에서 영화 데이터 가져오기
        movies = Movie.objects.all()
        if not movies:
            self.stdout.write(self.style.ERROR("데이터베이스에 영화가 없습니다. seed_movies를 먼저 실행하세요."))
            return

        documents = []
        ids = []
        
        self.stdout.write(f"총 {len(movies)}개의 영화를 학습합니다...")

        # 2. 텍스트 데이터 만들기 (제목 + 줄거리 + 장르 + 배우)
        for movie in movies:
            content = f"제목: {movie.title}\n장르: {movie.genre}\n감독: {movie.director}\n주연: {movie.actors}\n평점: {movie.vote_average}\n줄거리: {movie.overview}"
            documents.append(content)
            ids.append(str(movie.pk))

        # 3. 임베딩 & 벡터 저장 (Upstage Embedding 사용)
        # 저장 경로: 프로젝트 폴더 내 'chroma_db'
        persist_directory = os.path.join(settings.BASE_DIR, 'chroma_db')
        
        embeddings = UpstageEmbeddings(
            api_key=settings.UPSTAGE_API_KEY,
            model="solar-embedding-1-large"
        )

        # 기존 DB가 있다면 삭제하고 새로 생성 (간단한 구현을 위해)
        if os.path.exists(persist_directory):
            import shutil
            shutil.rmtree(persist_directory)

        vector_store = Chroma.from_texts(
            texts=documents,
            embedding=embeddings,
            ids=ids,
            persist_directory=persist_directory
        )

        self.stdout.write(self.style.SUCCESS(f"학습 완료! 데이터가 '{persist_directory}'에 저장되었습니다."))