from collections import namedtuple
import requests

from typing import Union
from random import randint, choice

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from bs4 import BeautifulSoup as BS

from app.database import SessionLocal
from app import models as m
from app import schemas as s


templates = Jinja2Templates(directory="app/templates")

MovieInfo = namedtuple("MovieInfo", ["title", "published_at", "running_time",  "category", "img"])

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def crawl_movie(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    data = requests.get(url, headers=headers)
    soup = BS(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    img = soup.select_one('meta[property="og:image"]')['content']
    category = soup.select_one(
        '#mainContent > div > div.box_basic > div.info_detail > div.detail_cont > div:nth-child(1) > dl:nth-child(3) > dd'
    ).get_text()
    published_at = soup.select_one(
        '#mainContent > div > div.box_basic > div.info_detail > div.detail_cont > div:nth-child(1) > dl:nth-child(1) > dd'
    ).get_text()
    running_time = soup.select_one(
        '#mainContent > div > div.box_basic > div.info_detail > div.detail_cont > div:nth-child(1) > dl:nth-child(5) > dd'
    ).get_text(strip=True)
    total_audience = soup.select_one(
        '#mainContent > div > div.box_basic > div.info_detail > div.detail_cont > div:nth-child(2) > dl:nth-child(2) > dd'
    ).get_text()

    return MovieInfo(
        title=title,
        published_at=published_at,
        total_audience=total_audience,
        running_time=running_time,
        category=category,
        img=img,
    )


@app.get("/movies/", response_class=HTMLResponse)
def movie_list(request: Request, category: Union[str, None] = None, db: Session = Depends(get_db)):
    if category:
        movies = db.query(m.Movie).filter(m.Movie.category == category).all()
    else:
        movies = db.query(m.Movie).all()

    first, second, third = db.query(m.Movie).order_by(m.Movie.rating.desc())[:3]
    context = {
        'request': request,
        'movies': movies,
        'first': first,
        'second': second,
        'third': third,
    }
    return templates.TemplateResponse('index.html', context)


@app.post('/movies/', response_model=s.Movie)
def create_movie(movie: s.MovieWrite, db: Session = Depends(get_db)):
    crawled_movie = crawl_movie(movie.url)

    db_movie = m.Movie(title=crawled_movie.title,
                       img=crawled_movie.img,
                       published_at=crawled_movie.published_at,
                       rating=movie.rating,
                       comment=movie.comment,
                       category=crawled_movie.category)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@app.get('/movies/{movie_id}/', response_model=s.Movie, name='detail')
def movie(request: Request, movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(m.Movie).filter(m.Movie.id == movie_id).first()
    context = {'request': request, 'movie': movie}
    return templates.TemplateResponse('detail.html', context)


@app.get('/dummy/', response_model=s.Movie)
def dummy(db: Session = Depends(get_db)):
    dummy_list = [
        "https://movie.daum.net/moviedb/main?movieId=129156",
        "https://movie.daum.net/moviedb/main?movieId=167558",
        "https://movie.daum.net/moviedb/main?movieId=169517",
        "https://movie.daum.net/moviedb/main?movieId=154241",
        "https://movie.daum.net/moviedb/main?movieId=135762",
        "https://movie.daum.net/moviedb/main?movieId=159863",
        "https://movie.daum.net/moviedb/main?movieId=163878",
        "https://movie.daum.net/moviedb/main?movieId=151324",
        "https://movie.daum.net/moviedb/main?movieId=162386",
        "https://movie.daum.net/moviedb/main?movieId=161806",
        "https://movie.daum.net/moviedb/main?movieId=167387",
        "https://movie.daum.net/moviedb/main?movieId=160409",
        "https://movie.daum.net/moviedb/main?movieId=151655",
        "https://movie.daum.net/moviedb/main?movieId=168706",
        "https://movie.daum.net/moviedb/main?movieId=166592"
    ]
    for url in dummy_list:
        crawled_movie = crawl_movie(url)

        db_movie = m.Movie(title=crawled_movie.title,
                           img=crawled_movie.img,
                           published_at=crawled_movie.published_at,
                           rating=randint(1, 10),
                           running_time=crawled_movie.running_time,
                           comment=choice(['재미있어요', '재미없어요', '돈 주고 보기 아까워요', '돈 많으면 보러가세요', '꼭 보세요']),
                           category=crawled_movie.category)
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
