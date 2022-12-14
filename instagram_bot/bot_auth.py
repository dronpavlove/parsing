from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from my_data import username, password
import time
import random


# def login(username, password):
#     browser = webdriver.Chrome('../chromedriver/chromedriver')
#
#     try:
#         browser.get('https://www.instagram.com')
#         time.sleep(random.randrange(3, 5))
#
#         username_input = browser.find_element_by_name('username')
#         username_input.clear()
#         username_input.send_keys(username)
#
#         time.sleep(2)
#
#         password_input = browser.find_element_by_name('password')
#         password_input.clear()
#         password_input.send_keys(password)
#
#         password_input.send_keys(Keys.ENTER)
#         time.sleep(10)
#
#         browser.close()
#         browser.quit()
#     except Exception as ex:
#         print(ex)
#         browser.close()
#         browser.quit()
#
#
# login(username, password)


def hashtag_search(username, password, hashtag):

    browser = webdriver.Chrome('../chromedriver/chromedriver')

    # try:
    #     browser.get('https://www.ok.ru/dk?st.cmd=anonymMain')
    #     time.sleep(random.randrange(3, 5))
    #
    #     email_input = browser.find_element_by_name('st.email')
    #     email_input.clear()
    #     email_input.send_keys(username)
    #
    #     time.sleep(2)
    #
    #     password_input = browser.find_element_by_name('st.password')
    #     password_input.clear()
    #     password_input.send_keys(password)
    #
    #     password_input.send_keys(Keys.ENTER)
    #     time.sleep(5)

    try:
        browser.get('https://horo.mail.ru/prediction/pisces/today/?frommail=1')
        time.sleep(5)  # find_element_by_css_selector
        text = browser.find_element_by_class_name('article__item.'
                                                  'article__item_alignment_left.article__item_html')
        for i in text.find_elements_by_tag_name('p'):
            print(i.text)

            # for i in range(1, 4):
            #     browser.execute_script("")
            #     time.sleep(random.randrange(3, 5))
            #
            # hrefs = browser.find_elements_by_tag_name('a')
            # posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            # posts_urls = []
            # for item in hrefs:
            #     href = item.get_attribute('href')
            #
            #     if "/p/" in href:
            #         posts_urls.append(href)
            #         print(href)

            # for url in posts_urls:
            #     try:
            #         browser.get(url)
            #         time.sleep(3)
            #         like_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
            #         time.sleep(random.randrange(80, 100))
            #     except Exception as ex:
            #         print(ex)

        browser.close()
        browser.quit()

        # except Exception as ex:
        #     print(ex)
        #     browser.close()
        #     browser.quit()

    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


hashtag_search(username, password, 'surfing')
