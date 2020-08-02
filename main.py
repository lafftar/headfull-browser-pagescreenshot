from selenium import webdriver

def init_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=socks5://154.21.232.12:11077')
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=8000")
    options.add_argument("user-data-dir=profile1")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options,
                              executable_path=rf'chromedriver_win32\chromedriver.exe')
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.set_window_size(1200, 8000)
    return driver