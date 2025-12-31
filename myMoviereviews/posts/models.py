from django.db import models

class Review(models.Model):
    GENRE_CHOICES = [
        ("action", "액션"),
        ("drama", "드라마"),
        ("comedy", "코미디"),
        ("thriller", "스릴러"),
        ("romance", "로맨스"),
        ("sf", "SF"),
        ("horror", "호러"),
        ("animation", "애니메이션"),
        ("etc", "기타"),
    ]

    RATING_CHOICES = [
        (1.0, "1"),
        (1.5, "1.5"),
        (2.0, "2"),
        (2.5, "2.5"),
        (3.0, "3"),
        (3.5, "3.5"),
        (4.0, "4"),
        (4.5, "4.5"),
        (5.0, "5"),
    ]

    title = models.CharField("제목", max_length=100)
    year = models.PositiveIntegerField("개봉년도")
    genre = models.CharField("장르", max_length=20, choices=GENRE_CHOICES)
    rating = models.DecimalField("별점", max_digits=2, decimal_places=1, choices=RATING_CHOICES)
    runtime = models.PositiveIntegerField("러닝타임(분)")
    content = models.TextField("리뷰")

    director = models.CharField("감독", max_length=100)
    actors = models.CharField("배우", max_length=200)

    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    def __str__(self):
        return self.title
