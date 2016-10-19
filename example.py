# coding:utf-8
import anitube

if __name__ == "__main__":
    soup = anitube.Anitube("fate")
    for idx, url in enumerate(soup.getMovieURL()):
        print(soup.titles[idx])
        print(soup.thumbnails[idx])
        print(url)
