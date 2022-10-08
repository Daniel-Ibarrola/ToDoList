from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

	def ger_error_element(self):
		return self.browser.find_element_by_css_selector(".has-error")

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

	def test_cannot_add_duplicate_items(self):
		self.browser.get(self.live_server_url)
		self.add_list_item("Buy wellies")

		self.get_item_input_box().send_keys("Buy wellies")
		self.get_item_input_box().send_keys(Keys.ENTER)

		# We should see an error message after trying to submit a
		# duplicate item
		self.wait_for(lambda: self.assertEqual(
			self.ger_error_element().text,
			"You've already got this in your list"
		))

	def test_error_messages_are_cleared_on_input(self):
		# Edith starts a list and causes a validation error
		self.browser.get(self.live_server_url)
		self.add_list_item("Banter too thick")
		self.get_item_input_box().send_keys("Banter too thick")
		self.get_item_input_box().send_keys(Keys.ENTER)

		self.wait_for(lambda: self.assertTrue(
			self.ger_error_element().is_displayed()
		))

		# She starts typing in the input box to clear the error
		self.get_item_input_box().send_keys("a")

		# She is pleased to see that the error message disappears
		self.wait_for(lambda: self.assertFalse(
			self.ger_error_element().is_displayed()
		))
