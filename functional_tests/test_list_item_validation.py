from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		# Trying to input an empty item should show an error on the page
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'))

		# Should be able to add non-empty items
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'))

		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# And then submit another blank item and see the error again
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'))

		# Add more items
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')
