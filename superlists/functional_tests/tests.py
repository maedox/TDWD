from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Katja has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        # She types "Buy cotton fabric" into a text box (Katja's hobby
        # is sewing children's clothes)
        inputbox.send_keys("Buy cotton fabric")

        # When she hits Enter, she is taken to a new URL,
        # and now the page lists "1: Buy cotton fabric" as an item in a
        # to-do list
        inputbox.send_keys(Keys.ENTER)
        katja_list_url = self.browser.current_url
        self.assertRegex(katja_list_url, "/lists/.+")
        self.check_for_row_in_list_table("1: Buy cotton fabric")

        # There is still a text box inviting her to add another item. She
        # enters "Use cotton fabric to make a dress" (Katja is very methodical)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use cotton fabric to make a dress")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table("2: Use cotton fabric to make a dress")
        self.check_for_row_in_list_table("1: Buy cotton fabric")

        # Now a new user, Pål, comes along to the site
        self.browser.quit()
        ## We use a new browser session to make sure that no information
        ## of Katja's is coming through from cookies etc.
        self.browser = webdriver.Firefox()

        # Pål vists the home page. There's no sign of Ketja's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Buy cotton fabric", page_text)
        self.assertNotIn("make a dress", page_text)

        # Pål starts a new list by entering a new item. He is less
        # interesting than Katja
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Pål gets his own unique URL
        pal_list_url = self.browser.current_url
        self.assertRegex(pal_list_url, '/lists/.+')
        self.assertNotEqual(pal_list_url, katja_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy cotton fabric', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, she goes back to sleep
