# This is a Python script for a Web Crawler that scrapes top 100 Google Search Results for specific keywords
# Importing Packages and Libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd


def get_keywords():
    try:
        # Reading keywords from file
        df = pd.read_csv('keywords.csv')
    except FileNotFoundError:
        print('File not Found...')
    else:
        # Dataframe to List
        return df['keywords'].to_list()


def page_transition():
    # initiating page transition
    elm = driver.find_element(By.LINK_TEXT, "Next")
    # elm.click()
    next_url = elm.get_attribute('href')
    present = False
    while not present:
        driver.get(next_url)
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'hlcw0c'))
            if element_present:
                present = True
                print(element_present)
            WebDriverWait(driver, 120).until(element_present)
        except TimeoutException:
            driver.get(next_url)
            print('Exception Occurred')

    # time.sleep(10)
    # wait for URL to change with 15 seconds timeout
    # try:
    #     WebDriverWait(driver, 15).until(EC.url_changes(current_url))
    # except Warning:
    #     print('URL not changed')


if __name__ == '__main__':

    path = 'F:\\edgedriver_win64\\msedgedriver.exe'
    driver = webdriver.Edge(path)
    wait = WebDriverWait(driver, 60)

    # Max number of results to be fetch
    def_MAX = 100
    keywords_list = get_keywords()

    for keyword in keywords_list:
        driver.get('https://www.google.com/')
        input_elements = driver.find_elements_by_css_selector('input[name=q]')
        input_elements[0].send_keys(keyword)
        input_elements[0].send_keys(Keys.ENTER)
        # for element in input_elements:
        #     element.send_keys(keyword)
        #     element.send_keys(Keys.ENTER)

        rank = 1
        results_df = pd.DataFrame()
        while rank <= def_MAX:

            # s = HTMLSession()
            # r.html.render(sleep=0.9)
            # r = s.get(current_url)
            # links = r.html.find('#rso', first=True)
            # print(links.html)

            # save current page url
            current_url = driver.current_url
            try:
                element_present = EC.presence_of_element_located((By.ID, 'rso'))
                WebDriverWait(driver, 300).until(element_present)
                page_source = driver.find_element_by_id('rso')
            except NoSuchElementException:
                print("Element Not Found")
            except TimeoutException:
                print('Timeout Exception Occurs')
            finally:
                page_html = page_source.get_attribute('innerHTML')
                soup = BeautifulSoup(page_html, 'html.parser')
            # print(soup.prettify())
            try:
                tg = soup.find_all(attrs={"class": "g kno-kp mnr-c g-blk"})
                tg[0].replace_with("")
            except:
                print()
            finally:
                fd = soup.find_all(attrs={"class": "yuRUbf"})
                for f in fd:
                    title = f.find("h3", class_="LC20lb DKV0Md").find('span').text
                    url = f.find('a').get('href')
                    print(keyword, rank, title, url)
                    dic = {'Keyword': keyword, 'Rank': rank, 'Title': title, 'URL': url}

                    # Appending dictionary to dataframe
                    results_df = results_df.append(dic, ignore_index=True)
                    rank = rank + 1

                    # Break inner loop if maximum results are fetched
                    if rank > def_MAX:
                        break
                else:
                    # initiating page transition
                    page_transition()
                    continue
                break
        # Appending results of one keyword to csv file
        results_df.to_csv('link.csv', mode='a', header=True, index=False, encoding="utf-8-sig")
