"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com

"""
"""
The formatter module focuses on processing raw text and returning it in 
the required format. 
"""

from datetime import datetime
import math
import pytz
import re
import pyshorteners


def formatResult(website, titles, prices, links, ratings, ratingsCount):
    """
    The formatResult function takes the scraped HTML as input, and extracts the 
    necessary values from the HTML code. Ex. extracting a price '$19.99' from
    a paragraph tag.
    :param website: website to scrape
    :param titles: title of the product
    :param prices: price of the product
    :param links: link of the product
    :param ratings: ratings of the product
    return: formatted result of the product
    """

    # the default values when the data is not available in scrapped
    title, price, link, rating, ratingCount = '', '', '', '', ''
    # websites
    if website == "target":
        title = titles
    elif website == "walmart":
        if titles:
            title = titles.get_text().strip()
    else:
        if titles:
            title = titles[0].get_text().strip()

    if website == "target":
        price = prices
    elif website == "eBay":
        price = prices[0].get_text().strip()
    else:
        if prices:
            price = prices[0].get_text().strip()
            price = re.search(r"\S+\d[\d,\.]*?\b", price)
            if price: 
                price=price.group()
            else: price='N/A'
            
            
    if website == "target":
        link = links
    elif website == "walmart":
        if links:
            link = links[0]['href']
            if link.startswith('/'):
                link = f'www.{website}.com{link}'
    elif website == "costco" or website == "eBay":
        if links:
            link = links[0]['href']
    else:
        if links:
            link = links[0]['href']
            link = f'www.{website}.com{link}'
    link = linkShortener(link)

    if website == "target":
        rating = ratings
    elif website == "walmart":
        if ratings:
            rating = ratings[0].get_text().split()[1]
    elif website == "costco":
        if ratings:
            if ratings[0].get_text() == "No Reviews":
                rating = 0
            else:
                temp = ratings[0].get_text().split()
                if len(temp) > 1:
                    rating = temp[1]
                else:
                    rating = "N.A"
    else:
        if ratings:
            rating = ratings[0].get_text().split()[0]

    if website == "target":
        ratingCount = ratingsCount
    else:
        if ratingsCount:
            ratingCount = ratingsCount[0].get_text().split()[0]
    product = {
        'timestamp':
        datetime.now(
            pytz.timezone('US/Eastern')).strftime("%d/%m/%Y %H:%M:%S %Z %z"),
        "title":
        formatTitle(title),
        "price":
        price if price != '' else 'N.A',
        "website":
        website,
        "rating":
        rating if rating != '' else 'N.A',
        "ratingCount":
        ratingCount if ratingCount != '' else 'N.A',
        "link":
        f'www.{website}.com{link}',
        "link":
        link
    }
    return product


def sortList(arr, sortBy, reverse):
    """
    The sortList function is used to sort the products list based on the
    flags provided as args. Currently, it supports sorting by price.
    :param arr: input array
    :param sortBy: sort by parameter
    :param reverse: flag to reverse the sort order
    return: result array
    """
    if sortBy == "pr":
        return sorted(arr,
                      key=lambda x: getNumbers(x["price"]),
                      reverse=reverse)
    elif sortBy == "ra":
        return sorted(arr,
                      key=lambda x: getNumbers(x.get("rating", '')),
                      reverse=reverse)
    elif sortBy == "all":
        return sorted(
            arr,
            key=lambda x:
            (getNumbers(x["price"]), getNumbers(x.get("rating", ''))),
            reverse=True)
    return arr


def formatSearchQuery(query):
    """
    The formatSearchQuery function formats the search string into a string that 
    can be sent as a url paramenter.
    :param query: input query
    return: replaced string
    """
    return query.replace(" ", "+")


def formatTitle(title):
    """
    The formatTitle function formats titles extracted from the scraped HTML code.
    :param title: title to format
    return: formatted title
    """
    if (len(title) > 40):
        return title[:40] + "..."
    return title


def getNumbers(st):
    """
    The getNumbers function extracts float values (price) from a string.
    Ex. it extracts 10.99 from '$10.99' or 'starting at $10.99'
    :param st: price string
    :return number
    """
    if type(st) == str:
        ans = ''
        if st == 'N.A':
            return -math.inf
        for ch in st:
            if (ch >= '0' and ch <= '9') or ch == '.':
                ans += ch
        try:
            ans = float(ans)
        except:
            ans = -math.inf
        return ans
    else:
        return st


def linkShortener(long_url):
    """
    The linkShortener function shortens the url of the item.
    :param long_url: The long version of the url being shortened
    """
    if not bool(long_url):
        return "https://www.ncsu.edu/"
    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(long_url)
    return short_url
