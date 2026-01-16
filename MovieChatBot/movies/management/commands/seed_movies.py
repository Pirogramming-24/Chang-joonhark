from django.core.management.base import BaseCommand
from movies.utils import fetch_and_save_movies

class Command(BaseCommand):
    help = 'TMDB에서 인기 영화 데이터를 가져와 DB에 저장합니다.'

    def handle(self, *args, **kwargs):
        self.stdout.write("영화 데이터 수집을 시작합니다...")
        fetch_and_save_movies()
        self.stdout.write(self.style.SUCCESS("수집 완료!"))