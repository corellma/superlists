from selenium import webdriver
from .base import FunctionalTest
from .lists_page import ListPage
from .my_lists_page import MyListsPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    def test_can_share_a_list_with_another_user(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session("edith@example.com")
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Her friend Onificerous is also hanging out on the lists site
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session("oniciferous@example.com")

        # Edith goes to the home page and starts a list
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item("get help")

        # She notices a "share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute("placeholder"), "friend@example.com"
        )

        # She shares her list.
        # The page updates to say that it's shared with Oniciferous:
        list_page.share_list_with("oniciferous@example.com")

        # Oniciferous now goes to the lists page with his browser
        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page()

        # He sees Edith's list there
        self.browser.find_element_by_link_text("get help").click()

        # On the list page, Oniciferous can see that it's Edith's list
        self.wait_for(
            lambda: self.assertIn("edith@example.com", list_page.get_list_owner())
        )