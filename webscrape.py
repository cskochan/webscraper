from bs4 import BeautifulSoup
import requests

def main():
    htmlText = requests.get("http://books.toscrape.com/index.html").text
    soup = BeautifulSoup(htmlText, 'lxml')
    genre_url = menuPick(soup)
    print(genre_url)

def menuPick(soup):
    navbar = soup.find('ul', class_ = "nav nav-list").li.ul.find_all('li')
    genre_dict = {'all': "http://books.toscrape.com/index.html"}
    for genre in navbar:
        name = genre.text.strip()
        print(name)
        genre_dict[name.lower()] = genre.a['href'.strip()]
    print('Please select a category (or enter "All" for all books).')
    genrePick = input("Genre: ").lower()
    if genrePick in genre_dict:
        return genre_dict[genrePick]
        
def write():
    pass

if __name__ == '__main__':
    main()