from re import sub
from time import time
from io import BytesIO
from PIL import Image
from  main import init_chrome
from selenium.common.exceptions import NoSuchElementException


def calc_height_and_scrolls(scroll_height=3700, max_height=1000):
    # when the scroll_height is not prime.
    for ideal_height in range(max_height, 500, -1):  # loop from highest val
        num_scrolls = scroll_height / ideal_height
        if num_scrolls.is_integer():
            return {
                "Ideal Height": int(ideal_height),
                "Ideal Scroll Num": int(num_scrolls)
            }

    # should only come to this block if it can't find a whole number.
    last_remainder = 1000
    closest_nums = {}
    for ideal_height in range(max_height, 500, -1):
        num_scrolls = scroll_height / ideal_height
        remainder = scroll_height % ideal_height
        if remainder < last_remainder:
            last_remainder = remainder
            closest_nums = {
                "Ideal Height": int(ideal_height),
                "Ideal Scroll Num": int(num_scrolls)
                }
            if remainder == 1: # the lowest remainder we're gonna get from a prime num
                break
    return closest_nums


def save_full_page_screenshot(driver, output_path):
    scroll_height = driver.execute_script("return "
                                          "document.getElementById('content').scrollHeight")
    # might be an optional thing
    navbar_height = driver.execute_script("return document"
                                          ".getElementsByClassName('h100')[0].scrollHeight")
    window_height = driver.execute_script("return window.innerHeight")
    final_img_height = scroll_height
    topmost_part = Image.open(BytesIO(driver.find_element_by_id("content").screenshot_as_png))
    final_image = Image.new('RGB', (topmost_part.width, final_img_height))
    final_image.paste(topmost_part, (0, 0))
    ideal_nums = calc_height_and_scrolls(scroll_height)
    ideal_height = ideal_nums['Ideal Height']
    driver.set_window_size(1200, ideal_height)
    paste_height = 0
    next_part = 0
    for scrolls in range(1, ideal_nums['Ideal Scroll Num'] + 1):
        # Issue calculating scroll height. It's missing some items. I'm scrolling by height of the entire window.
        # Account for height of top part of browser.
        driver.execute_script(f"window.scrollTo(0, {(window_height - navbar_height) * scrolls});")
        next_part = Image.open(BytesIO(driver.find_element_by_id("content").screenshot_as_png))
        next_part = next_part.crop((0, navbar_height, topmost_part.width, next_part.height))
        paste_height = (scrolls * next_part.height)
        final_image.paste(next_part, (0, paste_height))
    final_img_height = paste_height + next_part.height
    final_image.crop((0, 0, next_part.width, final_img_height))
    final_image.save(output_path)


def test():
    driver = init_chrome()
    driver.get("https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python-taking-union-o?rq=1")

    # get rid of coverings
    try:
        driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[4]').click()
    except NoSuchElementException:
        pass

    # make sure whatever you put here doesn't have special characters in it.
    path = f"{sub('[^A-Za-z0-9]+', ' ', driver.title)}.jpg"
    t1 = time()
    save_full_page_screenshot(driver, path)
    t2 = time()
    print(t2-t1)

    # hang the program to check the page
    input()
    driver.close()
    driver.quit()

test()