# Scrapper

Scrapper is a web scrapper that can scrape and extract information from any website. It's designed to be fast and efficient, making it easy for you to gather the data you need quickly and easily.Specifically it is designed for
- [E.Leclerc](https://www.e.leclerc/) and more specifically for scraping details of all the products of [Sports section](https://www.e.leclerc/cat/sport-loisirs) and [Jwellery section](https://www.e.leclerc/cat/vetements).

The data is stored locally on the mongodb database and some Queries are created to analyze the data.

## Features

- Ability to extract data from multiple websites at once, pagination is handled vey well.
- Easy-to-use interface with well organised code structure and proper object oriented approach.
- Fast and efficient performance, even when handling large amounts of data.
- All the features of [scrapy](https://scrapy.org/) comes very handy during the development and the code writing. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need the following software installed on your computer to run Scrapper:

- [Python](https://www.python.org/downloads/) (version 3.x or later)
- [scrapy](https://scrapy.org/)
- [Pymongo](https://pypi.org/project/pymongo/)
- [MongoDB Compass](https://www.mongodb.com/products/compass)
- [Git](https://git-scm.com/)
- Having the [Anaconda](https://www.anaconda.com/) installed will be a plus, as it is easy to manage virtual environments in Anaconda, but it's not necassory

### Installing

1. Clone or download the repository to your local machine.
    ```
    git clone https://github.com/Harsh324/Scrapper.git
    ```
2. Navigate to the directory where you have cloned or extracted the repository.
    ```
    cd Scrapper
    ```
3. Install the required dependencies and make sure that mongoDB is working and connection is on.


### Working

1. Now all the prerequistes are fixed, we need to run the scrapy spider to crawl and scrap the data, it takes around 45 - 50 minutes to scrap all the data of sports section and jwellery section.

2. Now run the following commands and wait for approx 40 - 50 minutes to finish the process of scraping all the data
    ```
    cd scrap_Eleclerc
    scrapy crawl scrapit
    ```

3. Now, In the same directory there is the file ```runQuery.py``` one can write the query there and run the file py wrting the command 
    ```
    python runQuery.py
    ```

4. The result of Query will be output on the terminal
## Built With

- [Python](https://www.python.org/)
- [scrapy](https://scrapy.org/)
- [Pymongo](https://pypi.org/project/pymongo/)
- [MongoDB](https://www.mongodb.com/)


## Authors

- [Harsh](https://github.com/Harsh324) - Initial work

