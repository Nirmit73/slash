"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com

"""

import formatter
import math
import urllib3


def test_formatSearchQuery():
    """
    Checks the formatSearchQuery function
    """
    assert formatter.formatSearchQuery("1 2") == "1+2"
    assert formatter.formatSearchQuery("A B") == "A+B"
    assert formatter.formatSearchQuery("ABC") == "ABC"
    assert formatter.formatSearchQuery(" AB") == "+AB"


def test_formatTitle():
    """
    Checks the formatTitle function
    """
    assert formatter.formatTitle("0" * 41) == "0" * 40 + "..."
    assert formatter.formatTitle("0" * 40) == "0" * 40
    assert formatter.formatTitle("0" * 5) == "0" * 5


def test_getNumbers():
    """
    Checks the getNumbers function
    """
    assert formatter.getNumbers(15) == 15
    assert formatter.getNumbers('N.A') == -math.inf
    assert formatter.getNumbers('$10.99') == 10.99
    assert formatter.getNumbers('test ABC5.39ABC test') == 5.39
    assert formatter.getNumbers('5..50') == -math.inf
    assert formatter.getNumbers('5.50 test 5.50') == -math.inf


def test_linkShortener():
    """
    Checks the linkShortener function
    """
    assert formatter.linkShortener(None) == "https://www.ncsu.edu/"
    test_tiny = formatter.linkShortener("https://www.google.com/")
    http = urllib3.PoolManager()  # Some shortened url
    response = http.request('GET', test_tiny)
    assert response.status == 200  # Checks site is successfully pulled
