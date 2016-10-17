# coding:utf-8
import anitube
import flask
if __name__ == "__main__":
    soup = anitube.Anitube("tekketsu")
    for url in soup.getMovieURL():
        print(url)
