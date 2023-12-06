from selenium import webdriver
from urllib.parse import urlparse

def single(url, dir="", suffix=""):
    if suffix != "":
        suffix = "_" + suffix
    browser = webdriver.Firefox()

    domain = urlparse(url).netloc
    prot = url[:5].rstrip(":")
    browser.get(url)
    scname = dir + prot + "_" + domain + suffix + ".png"
    screenshot = browser.save_screenshot(scname)
    browser.quit()

def list(ls, dir="", suffix=""):
    if len(ls) == 0:
        print("Set empty")
        return
    if suffix != "":
        suffix = "_" + suffix
    browser = webdriver.Firefox()

    for url in ls:
        domain = urlparse(url).netloc
        prot = url[:5].rstrip(":")
        browser.get(url)
        scname = dir + prot + "_" + domain + suffix + ".png"
        screenshot = browser.save_screenshot(scname)
    browser.quit()