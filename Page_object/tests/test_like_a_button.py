from playwright.sync_api import Page

from Page_object.pages.like_a_button import LikeAButton


def test_like_a_button_exists(page:Page):
    like_a_button = LikeAButton(page)
    like_a_button.open()
    like_a_button.check_button_visible()



def test_like_a_button_click(page:Page):
    like_a_button = LikeAButton(page)
    like_a_button.open()
    like_a_button.click_the_button()
    like_a_button.check_result_text_is_("Submitted")