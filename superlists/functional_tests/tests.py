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

        # When she hits Enter, the page updates, and now the page lists
        # "1: Buy cotton fabric" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table("1: Buy cotton fabric")

        # There is still a text box inviting her to add another item. She
        # enters "Use cotton fabric to make a dress" (Katja is very methodical)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use cotton fabric to make a dress")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table("2: Use cotton fabric to make a dress")
        self.check_for_row_in_list_table("1: Buy cotton fabric")

        # Katja wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail("Finish the test!")

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep
