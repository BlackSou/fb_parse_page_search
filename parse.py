from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class FacebookCrawler:
    LOGIN_URL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=111'

    def __init__(self, login, password):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        self.login(login, password)

    def login(self, login, password):
        self.driver.get(self.LOGIN_URL)

        # wait for the login page to load
        self.wait.until(EC.visibility_of_element_located((By.ID, "email")))

        self.driver.find_element_by_id('email').send_keys(login)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('loginbutton').click()

        # wait for the main page to load
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div/form/div/div/div/div/input[2]")))
        except TimeoutException:
            pass
    time.sleep(1)
    def _get_friends_list(self):
        difs = self.driver.find_elements_by_xpath("//div[@class='_4p2o _87m1']")
        print(len(difs))
        return difs
    time.sleep(1)
    def get_friends(self):
        # navigate to "friends" page
        time.sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div/form/div/div/div/div/input[2]").send_keys("Petro")
        time.sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div/form/button").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[3]/div[2]/div/div/div[3]/div/div/div/div[1]/div/div/div/div/div[1]/div/a").click()
        # continuous scroll until no more new friends loaded
        print(len(self._get_friends_list()))
        num_of_loaded_friends = 0
        while True:
            print("scrol")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)
            try:
                self.wait.until(lambda driver: len(self._get_friends_list()) > num_of_loaded_friends)
                num_of_loaded_friends = len(self._get_friends_list())
            except TimeoutException:
                break  # no more friends loaded
            if num_of_loaded_friends > 50:
                break

        return self._get_friends_list()


if __name__ == '__main__':
    import json
    
    crawler = FacebookCrawler(login='taras1rozsilka@gmail.com', password='zeus12345')
    friends = []
    for friend in crawler.get_friends():
        img = friend.find_element_by_xpath(".//img[@class='_1glk _6phc img']").get_attribute("src")
        name = friend.find_element_by_xpath(".//a[@class='_32mo']").get_attribute("title")
        link = friend.find_element_by_xpath(".//a[@class='_32mo']").get_attribute("href")
        friends.append({
            'name' : name,
            'img' : img,
            'link' : link
        })
    with open("json_data.json", "w") as f:
        f.write(json.dumps(friends))
        f.close()