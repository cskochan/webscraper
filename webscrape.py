from bs4 import BeautifulSoup
import requests
import time
import datetime

def main():
    website = "http://books.toscrape.com"
    htmlText = requests.get(website).text
    soup = BeautifulSoup(htmlText, 'lxml')
    genre_url = menuPick(soup)
    resultsPage(f"{website}/{genre_url}")
    write("\n*****     *****     *****\n")

def menuPick(soup):
    navbar = soup.find('ul', class_ = "nav nav-list").li.ul.find_all('li')
    genre_dict = {'all': "index.html"}
    for genre in navbar:
        name = genre.text.strip()
        print(name)
        genre_dict[name.lower()] = genre.a['href'.strip()]
    print('Please select a category (or enter "All" for all books).')
    while(True):
        genrePick = input("Genre: ").lower()
        if genrePick in genre_dict:
            write(genrePick.upper())
            return genre_dict[genrePick]
        else:
            print("Invalid Entry. Please try again.")

def resultsPage(link):
    linkParts = link.split("/")
    htmlText = requests.get(link).text
    soup = BeautifulSoup(htmlText, 'lxml')
    entryCount = soup.find('form', class_ ='form-horizontal').strong.text
    print(f"{entryCount} entries in total.")
    books = soup.find_all('article', class_ = 'product_pod')
    write(str(datetime.datetime.now()))
    for book in books:
        title = book.div.img['alt'].strip()
        info = bookPage(f"{'/'.join(map(str, linkParts[:4]))}/{book.div.a['href'].strip('../')}")
        write(f"\"{title}\" costs {info[0]} and is {info[1]}")
        time.sleep(1)
    try:
        print(soup.find('li', class_="current").text.strip())
        next = soup.find('li', class_="next").a['href'].strip()
        choice = input("See next page? [Y/n]").lower()
        if choice == 'y' or choice == '':
            resultsPage(f"{'/'.join(map(str, linkParts[:-1]))}/{next}")
        else:
            print("Goodbye")
    except:
        pass

def bookPage(link) -> tuple:
    linkParts = link.split("/")
    price = availability = "NULL"
    htmlText = requests.get(link).text
    soup = BeautifulSoup(htmlText, 'lxml')
    price = soup.find('p', class_="price_color").text.strip("Â")
    availability = soup.find('p', class_="instock availability").text.strip()
    return price, availability

        
def write(text):
    with open("results.txt", "a") as file:
        file.write(f"{text}\n")

if __name__ == '__main__':
    main()