from selenium import webdriver
from bs4 import BeautifulSoup, element
from time import sleep
from discord import Webhook, RequestsWebhookAdapter, File

import webdav.client as wc
import requests
import re
import os

base_url = 'https://dnd.wizards.com'

dc_webhook_id = os.environ['DISCORD_WEBHOOK_ID']
dc_webhook_token = os.environ['DISCORD_WEBHOOK_TOKEN']

cloud_folder = 'DnD/Unearthed_Arcana/'

nextcloud_options = {
    'webdav_hostname': os.environ['WEBDAV_HOSTNAME'],
    'webdav_login':    os.environ['WEBDAV_LOGIN'],
    'webdav_password': os.environ['WEBDAV_PASSWORD']
}

client = wc.Client(nextcloud_options)

webhook = Webhook.partial(
    dc_webhook_id, dc_webhook_token, adapter=RequestsWebhookAdapter())


def get_remote_list():
    print('getting existing pdfs...')
    existing_list = client.list(cloud_folder)
    # -1 bc .list() includes the current directory
    print("{} pdfs already in the cloud.".format(len(existing_list) - 1))

    return [item[item.find('_') + 1:item.find('.pdf')] for item in existing_list]


def get_page():
    print('setting up selenium...')

    options = webdriver.FirefoxOptions()
    options.headless = True
    options.binary = os.environ['FIREFOX_BINARY']
    driver = webdriver.Firefox(options=options)

    print('selenium ready, querying page...')

    driver.get("{}/articles/unearthed-arcana".format(base_url))

    more_button = driver.find_elements_by_class_name('more-button')

    while more_button:
        print('expanding page...')
        driver.execute_script('arguments[0].click();', more_button[0])
        sleep(1)
        more_button = driver.find_elements_by_class_name('more-button')

    src = driver.page_source

    driver.quit()

    return src


def get_pdf(article):
    r = requests.get("{}{}".format(base_url, article.link))
    soup = BeautifulSoup(r.content, features='html.parser')

    button = soup.find('a', {'class': 'cta-button'})
    pdf_link = button['href']

    if not re.match(r".*wizards\.com/.*\.(pdf|PDF)$", pdf_link):
        print("No pdf download found for {}".format(
            article.get_original_name()))
        print(pdf_link)
        return None

    print("pulling {}...".format(pdf_link))

    pdf = requests.get(pdf_link)

    print("done.")

    return pdf.content


def upload_file(article, dir):
    file_path = "{}/{}.pdf".format(dir, article.name)

    print("uploading {}...".format(article.get_original_name()))

    client.upload_sync(
        remote_path="{}/{}.pdf".format(cloud_folder, article.name), local_path=file_path)
    os.remove(file_path)

    print("done.")

    notify_discord(article)


def notify_discord(article):
    webhook.send(
        "Edition **{}** of Unearted Arcana, **{}**, is now available on the mibra cloud. Check it out!".format(article.get_index(), article.get_original_name()))
