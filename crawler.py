from selenium import webdriver  # Web driver
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  # BeautifulSoup
import pandas as pd  # Python Pandas Library
from urllib.parse import urlparse, urljoin  # For Url functions

# Path of the web Driver
path = 'F:\\edgedriver_win64\\msedgedriver.exe'
driver = webdriver.Edge(path)


# 1. Function to find the title of the page
def page_title(page):
    try:
        titleOfPage = page.title.string
        return titleOfPage
    except AttributeError:
        return ''


# Title Lenght
def page_title_lenght(titleOfPage):
    try:
        return len(titleOfPage)
    except TypeError:
        return -1


# Keyword in title or not  ?
def keyword_in_title(keyword, titleOfPage):
    # presence of keyword in
    try:
        keyword = keyword.lower()
        titleOfPage = titleOfPage.lower()
        if titleOfPage.find(keyword) != -1:
            return 1
        words = keyword.split()
        for word in words:
            if titleOfPage.find(word) != -1:
                return 1
        return 0
    except AttributeError:
        return -1


# Title start with Keyword ?
def is_title_start_with_keyword(titleOfPage, keyword):
    try:
        keyword = keyword.lower()
        titleOfPage = titleOfPage.lower()
        if titleOfPage.startswith(keyword) == True:
            return 1
        words = keyword.split()
        for word in words:
            if titleOfPage.startswith(word) == True:
                return 1
        return 0
    except AttributeError:
        return -1


# Lenght of the Url
def lenght_of_url(myurl):
    return len(myurl)


# Keyword in Url or not ?
def keyword_in_url(url, keyword):
    keyword = keyword.lower()
    url = url.lower()
    if url.find(keyword) != -1:
        return 1
    words = keyword.split()
    for word in words:
        if url.find(word) != -1:
            return 1
    return 0


# Doamin name in Url
def domain_name(myurl):
    domainName = urlparse(myurl).netloc
    return domainName


# No of H1 Tags
def h1_tags(page):
    h1Tags = page.findAll('h1')
    return len(h1Tags)


# Keyword in H1 Tag present or not ?
def keyword_in_h1_tag(page, keyword):
    try:
        h1Tags = page.findAll('h1')
        keyword = keyword.lower()
        if (len(h1Tags) >= 1):
            for tags in h1Tags:
                tags = tags.text.strip().lower()
                if tags.find(keyword) != -1:
                    return 1
                words = keyword.split()
                for word in words:
                    if tags.find(word) != -1:
                        return 1
                return 0
        else:
            return 0
    except TypeError:
        return -1


# No of H2 Tags
def h2_tags(page):
    h2Tags = page.findAll('h2')
    return len(h2Tags)


def keyword_in_h2_tag(page, keyword):
    try:
        h2Tags = page.findAll('h2')
        keyword = keyword.lower()
        if (len(h2Tags) >= 1):
            for tags in h2Tags:
                tags = tags.text.strip().lower()
                if tags.find(keyword) != -1:
                    return 1
                words = keyword.split()
                for word in words:
                    if tags.find(word) != -1:
                        return 1
                return 0
        else:
            return 0
    except TypeError:
        return -1


# No of H3 Tags
def h3_tags(page):
    h3Tags = page.findAll('h3')
    return len(h3Tags)


def keyword_in_h3_tag(page, keyword):
    try:
        h3Tags = page.findAll('h3')
        keyword = keyword.lower()
        if (len(h3Tags) >= 1):
            for tags in h3Tags:
                tags = tags.text.strip().lower()
                if tags.find(keyword) != -1:
                    return 1
                words = keyword.split()
                for word in words:
                    if tags.find(word) != -1:
                        return 1
                return 0
        else:
            return 0
    except TypeError:
        return -1


# Content Lenght of webpage
def content_of_website(page):
    allText = page.find_all(text=True)
    content = ''
    textTags = ['p', 'div', 'a', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul',
                'ol', 'li', 'strong', 'blockquote', 'br']
    for text in allText:
        if text.parent.name in textTags:
            content += '{} '.format(text)
    return content


# Keyword Denisty
def denisty_of_keyword(keyword, content, contentLenght):
    if (contentLenght > 0):
        keyword = keyword.lower()
        content = content.lower()
        if (len(keyword.split()) == 1):
            if keyword in content:
                keywordOccur = content.count(keyword)
                keywordDenisty = round(((keywordOccur / contentLenght) * 100), 2)
                return keywordDenisty
        else:
            words = keyword.split()
            keywordOccur = 0
            for word in words:
                if word in content:
                    keywordOccur += content.count(word)
            keywordDenisty = round(((keywordOccur / contentLenght) * 100), 4)
            return keywordDenisty
        return 0
    else:
        return 0
    # Links Total,Internal and External Links Info


def links(page, url):
    internal_urls = []
    external_urls = []
    domain_name = urlparse(url).netloc
    urls = []
    for a_tag in page.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                external_urls.append(href)
            continue
        urls.append(href)
        internal_urls.append(href)

    return len(internal_urls), len(external_urls), len(external_urls) + len(internal_urls)


# Getting Description meta tag lenght and presence of Keyword in Description meta tag


def description_lenght(page_soup):
    try:
        meta = page_soup.find_all('meta')
        descriptionLenght = 0
        for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description']:
                descriptionLenght = len(tag.attrs['content'])
        return descriptionLenght
    except KeyError:
        return -1


def keyword_in_description(page_soup, keyword):
    try:
        meta = page_soup.find_all('meta')
        for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description']:
                keyword = keyword.lower()
                if (tag.attrs['content']).find(keyword) != -1:
                    return 1
        return 0
    except KeyError:
        return -1


# Total no images, Images with alt tag and images without alt tag


def no_of_images(page):
    try:
        images = page.findAll('img')
        imagesWithAltTag = 0
        imagesWithoutAltTag = 0
        count = 0
        for img in images:
            count += 1
            if img.has_attr('alt') == True:
                if img['alt']:
                    imagesWithAltTag += 1
                elif img['alt'] == "":
                    imagesWithoutAltTag += 1
            else:
                imagesWithoutAltTag += 1
        return imagesWithAltTag, imagesWithoutAltTag, count
    except KeyError:
        return -1, -1, count


# Keyword in all Images with their alt Tag


def keyword_in_img_altTag(page, keyword):
    try:
        images = page.findAll('img')
        count = 0
        for img in images:
            if img.has_attr('alt') == True:
                keyword = keyword.lower()
                img_alt_lower = img['alt'].lower()
                if img_alt_lower.find(keyword) != -1:
                    count += 1
            else:
                continue
        return count
    except KeyError:
        return -1


def main():
    df = pd.read_csv('links.csv', encoding="utf-8-sig")
    for index, row in df.iterrows():
        keyword = row['keyword']
        rank = row['rank']
        myurl = row['URL']
        titleOfPage = row['title']
        try:
            driver.get(myurl)

            # Getting page Source
            source = driver.page_source
            page_soup = BeautifulSoup(source, 'html.parser')

            # # Page Title
            # titleOfPage = page_title(page_soup)

            # Lenght of page Title
            lenghtOfTitle = page_title_lenght(titleOfPage)

            # Presence of keyword in title
            keywordInTitle = keyword_in_title(titleOfPage, keyword)

            # Keyword at start of title ?
            isTitleStartWithKeyword = is_title_start_with_keyword(
                keyword, titleOfPage)

            # Lenght of URL
            lenghtOfUrl = lenght_of_url(myurl)

            # Keyword presence in URL
            keywordInUrl = keyword_in_url(myurl, keyword)

            # Domain name
            domainName = domain_name(myurl)

            # No of h1 tags
            noOfH1Tags = h1_tags(page_soup)

            # keyword in H1 Tags
            keywordInH1Tags = keyword_in_h1_tag(page_soup, keyword)

            # No of H2 Tags
            noOfH2Tags = h2_tags(page_soup)

            keywordInH2Tags = keyword_in_h2_tag(page_soup, keyword)

            # No of H3 Tags
            noOfH3Tags = h3_tags(page_soup)

            keywordInH3Tags = keyword_in_h3_tag(page_soup, keyword)

            # content of whole website
            content = content_of_website(page_soup)

            # Content lenght of the website
            contentLenght = len(content)

            # Keyword Denisty
            keywordDenisty = denisty_of_keyword(keyword, content, contentLenght)

            # Description meta tag lenght and keyword presence in decsription
            keywordInDescription = keyword_in_description(
                page_soup, keyword)
            descriptionLenght = description_lenght(page_soup)

            # Total Images, images with alt Tag, images Without Alt Tag
            imagesWithAltTag, imagesWithoutAltTag, noOfImages = no_of_images(
                page_soup)

            # No Of images Having keyword in their Alt Tags
            keywordInImageAltTag = keyword_in_img_altTag(page_soup, keyword)

            # Total links, Internal Links, External Links
            internalLinks, externalLinks, totalLinks = links(page_soup, myurl)

            # presence of internal links
            if internalLinks >= 1:
                presenceOfInternalLink = 1
            else:
                presenceOfInternalLink = 0
            if externalLinks >= 1:
                presenceOfExternalLink = 1
            else:
                presenceOfExternalLink = 0

            # Making Dict
            result_dict = {'Keyword': [keyword], 'Rank': [rank], 'Title Of Page': [titleOfPage], 'Url': [myurl],
                           'Lenght Of Title': [lenghtOfTitle], 'Presence of Keyword in Title': [keywordInTitle],
                           'Title Starts with Keyword': [isTitleStartWithKeyword], 'Lenght of Url': [lenghtOfUrl],
                           'Presence Of Keyword In Url': [keywordInUrl], 'Domain Name': [domainName],
                           'No of H1 Tags': [noOfH1Tags], 'Presence of Keyword in H1 Tag': [keywordInH1Tags],
                           'No of H2 tags': [noOfH2Tags], 'Presence of Keyword in H2 Tag': [keywordInH2Tags],
                           'No of H3 Tags': [noOfH3Tags],
                           'Presence of Keyword in H3 Tag': [keywordInH3Tags], 'Content Lenght': [contentLenght],
                           'Keyword Denisty': [keywordDenisty], 'Lenght of Description': [descriptionLenght],
                           'Keyword in Description': [keywordInDescription], 'Total Images': [noOfImages],
                           'Images Without Alt Tags': [imagesWithoutAltTag], 'Images With Alt Tag': [imagesWithAltTag],
                           'Keyword in Alt Tags of Images': [keywordInImageAltTag], 'Total Links': [totalLinks],
                           'Internal Links': [internalLinks], 'External Links': [externalLinks],
                           'Presence of Internal Link': [presenceOfInternalLink],
                           'Presence of External Links': [presenceOfExternalLink]}

            # Creating data Frame
            df = pd.DataFrame(result_dict, columns=result_dict.keys())

            # saving the dataframe
            df.to_csv('dataset.csv', mode='a', header=False, index=False, encoding="utf-8-sig")

        except:
            error_dict = {'Keyword': [keyword], 'Rank': [rank], 'Title Of Page': [titleOfPage], 'URL': [myurl]}
            # Creating data Frame
            df = pd.DataFrame(error_dict, columns=error_dict.keys())
            # saving the dataframe
            df.to_csv('error_links.csv', mode='a', header=False, index=False, encoding="utf-8-sig")
            # continue


if __name__ == '__main__':
    main()
