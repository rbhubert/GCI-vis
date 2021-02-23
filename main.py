#!/usr/bin/env python3

import argparse

import tldextract
import validators

from config.valid_newspapers import mapping_newspaper, get_valid_newspaper_str


# This class will validate whether the url parameter is a valid url and if we have the crawler for that newspaper
# The newspaper has to be one of the ones inside mapping_newspaper
class ValidateURL(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        url = values
        valid = validators.url(url)
        if valid:
            str_page = tldextract.extract(url).domain
            valid_newspapers = mapping_newspaper.keys()
            if str_page in valid_newspapers:
                setattr(args, self.dest, url)
                setattr(args, "newspaper", mapping_newspaper[str_page])
            else:
                parser.error(
                    "We can't scrap '" + url + "' because we don't have that crawler yet. The newspaper has to be " + get_valid_newspaper_str())
        else:
            parser.error("'" + url + "' is not an valid url")


# Main defines the parameter for calling this script:
# -url is the url to be scrapped
# - lastComment is an optional parameter, that allows to get the new comments since the 'lastComment' id.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", help="The url to be scraped", required=True, action=ValidateURL)
    parser.add_argument('-lastComment',
                        help="ID of the last comment recovered for this url --> The new comments since lastComment will be retrieve")
    args = parser.parse_args()

    url = args.url
    newspaper = args.newspaper
    lastComment = args.lastComment

    if lastComment:
        print(newspaper.get_latest_comments(url, lastComment))
    else:
        print(newspaper.get_newsItem(url))


if __name__ == "__main__":
    main()
