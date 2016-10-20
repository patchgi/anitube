# coding:utf-8
import anitube

if __name__ == "__main__":
    soup = anitube.Anitube("shakunetsu")
    for idx in range(len(soup.movies)):
        print(soup.movies[idx])
        print(soup.thumbnails[idx])
        print(soup.titles[idx])
