# zipmatch-demo

This is a web scraper that gets Condo for Rent listings at Metro Manila posted at [ZipMatch](https://www.zipmatch.com/rent/condominium)

Disclaimer: This is done for demo purposes only and not intended for commercial use.

Target data:
1. Post title
1. Description
1. Unit details (floor area, amenities, etc.)
1. Date posted
1. Image links
1. Address and Geolocation


## Installing Scrapy

### via pip
`pip install scrapy`
### or via conda
`conda install scrapy`

## Running the spider
`scrapy crawl zipmatch_rent -o output.csv -t csv`

This would create and store the data into `output.csv`. The scraper is set to only get ~100 items for this demo.
