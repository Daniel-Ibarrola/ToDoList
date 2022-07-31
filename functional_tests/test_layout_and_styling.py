from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# The input box should be centered
		input_box = self.get_item_input_box()
		self.assertAlmostEqual(
			input_box.location['x'] + input_box.size['width'] / 2,
			512,
			delta=10
		)

		# The input box should be centered in the new list page too
		input_box.send_keys('testing')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		input_box = self.get_item_input_box()
		self.assertAlmostEqual(
			input_box.location['x'] + input_box.size['width'] / 2,
			512,
			delta=10
		)