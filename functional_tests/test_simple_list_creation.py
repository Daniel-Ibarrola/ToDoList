from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

	def test_can_start_a_list_for_one_user(self):
		self.browser.get(self.live_server_url)

		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		input_box = self.get_item_input_box()
		self.assertEqual(
			input_box.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		input_box.send_keys('Buy peacock feathers')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		input_box = self.get_item_input_box()
		input_box.send_keys('Use peacock feathers to make a fly')
		input_box.send_keys(Keys.ENTER)

		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

	def test_multiple_users_can_start_lists_at_different_urls(self):

		# Edit (the first user) goes to the website and starts a list
		self.browser.get(self.live_server_url)

		input_box = self.get_item_input_box()
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

		input_box = self.get_item_input_box()
		input_box.send_keys('Buy milk')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(edith_list_url, francis_list_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk',  page_text)
