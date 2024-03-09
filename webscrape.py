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

# Returns url for list of books in user-picked genre
def menuPick(soup) -> str:
    # Finds list of genres for user to pick from
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

# Scans books on page, follows each link
def resultsPage(link, manual = "n") -> None:
    linkParts = link.split("/") # split for easy piecing together of urls
    htmlText = requests.get(link).text
    soup = BeautifulSoup(htmlText, 'lxml')
    # We only want this to execute on page 1
    if(linkParts[-1] == "index.html"):
        entryCount = int(soup.find('form', class_ ='form-horizontal').strong.text)
        print(f"{entryCount} entries in total existing on {entryCount//20 + 1} page(s).")
        print("Would you like to scan one page at a time?")
        while(True):
            manual = input("[Y/n]: ").lower()
            if manual in ("y", "n", ""):
                break
            else:
                print("Unrecognized selection.")
        write(str(datetime.datetime.now()))
    # We want this to execut for every page of book
    books = soup.find_all('article', class_ = 'product_pod')
    for book in books:
        title = book.div.img['alt'].strip()
        # Sends book url to bookPage(), returning price and availability as a tuple
        info = bookPage(f"{'/'.join(map(str, linkParts[:4]))}/{book.div.a['href'].strip('../')}")
        write(f"\"{title}\" costs {info[0]} and is {info[1]}")
        time.sleep(1)
    # Tests if there are more pages, raises exception if not
    try:
        print(soup.find('li', class_="current").text.strip()) # Current page info does not exist on single page lists
        next = soup.find('li', class_="next").a['href'].strip() # Next button does not exist on final page
        if manual in ("y", ""):
            choice = input("See next page? [Y/n]").lower()
            if choice in ('y', ''):
                resultsPage(f"{'/'.join(map(str, linkParts[:-1]))}/{next}", manual)
            else:
                print("Goodbye")
        else:
            resultsPage(f"{'/'.join(map(str, linkParts[:-1]))}/{next}", manual)
    except:
        pass

# For use on a books page, returns price and availability of book
def bookPage(link) -> tuple:
    htmlText = requests.get(link).text
    soup = BeautifulSoup(htmlText, 'lxml')
    price = soup.find('p', class_="price_color").text.strip("Â") # Character exists before £ for some reason
    availability = soup.find('p', class_="instock availability").text.strip()
    return price, availability

        
def write(text) -> None:
    with open("results.txt", "a") as file:
        file.write(f"{text}\n")

if __name__ == '__main__':
    main()