import pandas as pd
from io import StringIO
from lxml import etree
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def google_pdf_parser(dict_links_full, dict_links, all_links, page, next_page_exist, parser, a_keyword, browser):
    while next_page_exist:
        try:
            page_xml = browser.page_source
            tree = etree.parse(StringIO(page_xml), parser)
            pdfki = tree.xpath(".//div[@class='g']")
            for a_link in range(0, len(browser.find_elements_by_xpath(".//div[@class='g']//h3/a[@href]"))-1):
                print(a_link, "  ", ''.join(pdfki[a_link].xpath(".//h3/a/@href")))
                if ''.join(pdfki[a_link].xpath(".//h3/a/@href")) not in all_links:
                    print(a_link)
                    print(pdfki[a_link].xpath(".//h3/a/@href"),
                          '\n',
                          pdfki[a_link].xpath('.//div[@class="f slp"]/text()'),
                          '\n',
                          pdfki[a_link].xpath('.//span[@class = "st"]/text()'),
                          '\n',
                          tree.xpath('//div[@id="resultStats"]/text()'),
                          '\n',
                          pdfki[a_link].xpath(
                              './/div[@class="f slp"]/a[@href][contains(text(), "Related articles")]/@href'),
                          '\n',
                          pdfki[a_link].xpath(
                              './/div[@class="f slp"]/a[@href][contains(text(), "Cited by")]/@href'),
                          '\n')
                    all_links.append(''.join(pdfki[a_link].xpath(".//h3/a/@href")))
                    dict_links.append({'pdf_link': ''.join(pdfki[a_link].xpath(".//h3/a/@href")),
                                       'title': ''.join(pdfki[a_link].xpath(".//h3/a[@href]/text()")),
                                       'google_page': page,
                                       'author_and_date': ''.join(
                                           pdfki[a_link].xpath('.//div[@class="f slp"]/text()')),
                                       'result_stats': ''.join(tree.xpath('//div[@id="resultStats"]/text()')),
                                       'pdf_cited_by': ''.join(pdfki[a_link].xpath(
                                           './/div[@class="f slp"]/a[@href][contains(text(), "Cited by")]/@href')),
                                       'pdf_related_articles': ''.join(pdfki[a_link].xpath(
                                           './/div[@class="f slp"]/a[@href][contains(text(), "Related articles")]/@href')),
                                       'pdf_snippets': ' '.join(
                                           pdfki[a_link].xpath('.//span[@class = "st"]/text()')),
                                       'keyword': keywords[i]})
            button = browser.find_element_by_xpath('//div[@id="foot"]//span[text()="Next"]')
            button.click()
            page += 1
            sleep(randint(5, 10))
        # except ElementNotSelectableException as err:
        #     print('\n', "ElementNotSelectableException !!!", '\n')
        #     sleep(randint(210, 220))
        #     google_pdf_parser(dict_links, all_links, page - 1, True, parser)
        except NoSuchElementException as e:
            sleep(15)
            print('Hey!I am here!')
            page_xml_1 = browser.page_source
            tree_1 = etree.parse(StringIO(page_xml_1), parser)
            I_am_not_a_robot = tree_1.xpath('//*[@id = "g-recaptcha-response"]')
            print(I_am_not_a_robot)
            if I_am_not_a_robot != []:
                print('I have got a captcha!')
                sleep(randint(45, 60))
                I_am_not_a_robot = []
                print('We solve the captcha! We are good!', '\n', 'I_am_not_a_robot = ', I_am_not_a_robot)
                google_pdf_parser(dict_links_full, dict_links, all_links, page - 1, True, parser, a_keyword, browser)
            else:
                print('Ura!', '\n', 'We are waiting for another keyword!!!')
                next_page_exist = False
    return dict_links


binary = FirefoxBinary('/usr/bin/firefox')
fp = webdriver.FirefoxProfile('/home/user/.mozilla/firefox/vmofja5l.default/')
browser = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary)
key_df = pd.read_csv('/home/user/PycharmProjects/Selenium/keywords.txt',
                     sep=',', header=None)
keywords = key_df[0].tolist()
browser.get("http://www.google.com/ncr")
dict_links_full = []
dict_links = []
all_links = []
parser = etree.HTMLParser()
table = pd.DataFrame(dict_links_full)
writer = pd.ExcelWriter('/home/user/PycharmProjects/Selenium/PDF_links/fumichev.xlsx')
table.to_excel(writer, 'links', index=False)
writer.save()

for i in range(0, len(keywords)):
    results = []
    a_keyword = keywords[i]
    page = 1
    elem = browser.find_element_by_name("q")
    elem.clear()
    sleep(randint(3, 5))
    elem.send_keys("%s" % keywords[i])  # in search box of the site
    elem.send_keys(Keys.RETURN)
    sleep(randint(3, 5))
    assert "No results found." not in browser.page_source
    next_page_exist = True
    dict_links_full = google_pdf_parser(dict_links_full, dict_links, all_links, page, next_page_exist, parser,
                                        a_keyword, browser)
    excel = pd.ExcelFile('/home/user/PycharmProjects/Selenium/PDF_links/fumichev.xlsx')
    exceltable = excel.parse('links')
    table3 = pd.DataFrame(dict_links_full)
    writer3 = pd.ExcelWriter('/home/user/PycharmProjects/Selenium/PDF_links/fumichev.xlsx', engine='openpyxl')
    concat = pd.concat([exceltable, table3], ignore_index=True)
    concat.to_excel(writer3, 'links', index=False,
                    columns=['pdf_link', 'keyword', 'google_page', 'result_stats', 'title',
                             'author_and_date', 'pdf_snippets', 'pdf_related_articles', 'pdf_cited_by'])
    writer3.save()
    sleep(randint(90, 210))