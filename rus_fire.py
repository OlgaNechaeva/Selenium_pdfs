# driver = webdriver.Firefox()
# driver.get("http://www.google.ru")
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("%s fileType: pdf" % keywords[0])  # in search box of the site
# elem.send_keys(Keys.RETURN)
# sleep(randint(3, 5))
# assert "No results found." not in driver.page_source
# link = driver.page_source
# elements = driver.find_elements_by_xpath("//h3/a[@href]")
# for element in elements:
#     if '.pdf' in element.get_attribute("href"):
#         results.append(element.get_attribute("href"))
#         print(element.get_attribute("href"))

#
# excel = pd.ExcelFile('/home/user/PycharmProjects/Selenium/PDF_links/%s.xlsx' % keywords[0])
# exceltable = excel.parse('Links')
# table1 = pd.DataFrame(results)
# writer1 = pd.ExcelWriter('/home/user/PycharmProjects/Selenium/PDF_links/%s.xlsx' % keywords[0],
#                          engine='openpyxl')
# concat = pd.concat([exceltable, table1], ignore_index=True)
# concat.to_excel(writer1, 'Links', index=False)
# writer1.save()



try:
    elements = browser.find_elements_by_xpath("//h3/a[@href]")
    for element in elements:
        if '.pdf' in element.get_attribute("href"):
            results.append(element.get_attribute("href"))
            print(element.get_attribute("href"))
            # if we need more than one column in the table
            dict_links.append({'links': element.get_attribute("href"),
                               'google_page': page,
                               'keyword': keywords[i]})
    button = browser.find_element_by_xpath('//div[@id="foot"]//span[text()="Next"]')
    button.click()
    page += 1
    sleep(randint(10, 15))
except NoSuchElementException as e:
    z = False
except InvalidElementStateException as err:
    sleep(randint(90, 210))


    pdf_links = browser.find_elements_by_xpath("//h3/a[@href]")
    pdf_authors_date = browser.find_elements_by_xpath('//div[@class="f slp"]')
    pdf_snippets = browser.find_elements_by_xpath('//span[@class = "st"]')
    pdf_cited_by = browser.find_elements_by_xpath('//div[@class="f slp"]/a[@href][1]')
    pdf_related_articles = browser.find_elements_by_xpath('//div[@class="f slp"]/a[@href][2]')
    pdf_site = browser.find_elements_by_xpath("//cite[@class='_Rm'][not(name()='b')]")
    result_stat = browser.find_elements_by_xpath('//div[@id="resultStats"]')
    link_num = 1
    for element in pdf_links:
        if '.pdf' in element.get_attribute("href"):
            results.append(element.get_attribute("href"))
            print(element.get_attribute("href"),
                  '\n',
                  pdf_cited_by[link_num].get_attribute("href"),
                  '\n',
                  pdf_authors_date[link_num].text,
                  '\n',
                  pdf_snippets[link_num].text,
                  '\n',
                  pdf_related_articles[link_num].get_attribute("href"),
                  '\n',
                  pdf_site[link_num].text,
                  '\n')
            # if we need more than one column in the table
            # dict_links.append({'links': element.get_attribute("href"),
            #                    'google_page': page,
            #                    'author_and_date': pdf_authors_date[link_num],
            #                    'result_stats': result_stat[0].text,
            #                    'pdf_cited_by': pdf_cited_by[link_num].get_attribute("href"),
            #                    'pdf_related_articles': pdf_related_articles[link_num].get_attribute("href"),
            #                    'pdf_snippets': pdf_snippets[link_num].text,
            #                    'pdf_is_from_site': pdf_site[link_num].text,
            #                    'keyword': keywords[i]}
            #                   )
            link_num += 1

    pdf_links = tree.xpath(".//div[@class='g'][2]//h3/a[@href]")[0].values()[0]
    pdf_authors_date = tree.xpath('.//div[@class="g"][9]//div[@class="f slp"]/text()')[0]
    pdf_snippets = tree.xpath('.//div[@class="g"][1]//span[@class = "st"]/text()')
    pdf_site = tree.xpath('.//div[@class="g"][1]//cite[@class="_Rm"]/text()')[0]
    result_stat = tree.xpath('//div[@id="resultStats"]/text()')[0]
    pdf_related_articles = tree.xpath('.//div[@class="g"][9]//div[@class="f slp"]/a[@href][2]')[0].values()[1]
    pdf_cited_by = tree.xpath('.//div[@class="g"][9]//div[@class="f slp"]/a[@href][1]')[0].values()[1]
