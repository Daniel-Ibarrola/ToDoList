from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
		self.browser.get(self.live_server_url)

		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			input_box.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		input_box.send_keys('Buy peacock feathers')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Use peacock feathers to make a fly')
		input_box.send_keys(Keys.ENTER)

		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

	def test_multiple_users_can_start_lists_at_different_urls(self):

		# Edit (the first user) goes to the website and starts a list
		self.browser.get(self.live_server_url)

		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Buy peacock feathers')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		# The second user, Francis, also starts a new list

		# We use a new browser session to ensure that no information of
		# Edit is coming through
		self.browser.quit()
		self.browser = webdriver.Firefox()
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Buy milk')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(edith_list_url, francis_list_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk',  page_text)

	def test_layout_and_styling(self):
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# The input box should be centered
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			input_box.location['x'] + input_box.size['width'] / 2,
			512,
			delta=10
		)

		# The input box should be centered in the new list page too
		input_box.send_keys('testing')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			input_box.location['x'] + input_box.size['width'] / 2,
			512,
			delta=10
		)
		