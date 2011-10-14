
from unittestzero import Assert

from details_page import DetailsPage



class TestPayment:

    def test_that_payment_is_made(self, mozwebqa):

        #For now, this is the addon used to test payment
        #https://addons-dev.allizom.org/en-US/firefox/addon/assistant/
        details_page = DetailsPage(mozwebqa, 'assistant')
        details_page.login()
        Assert.true(details_page.header.is_user_logged_in)
        Assert.contains("Assistant", details_page.title)
        details_page.click_add_to_firefox()
        Assert.contains("Purchase Add-on", details_page.purchase_modal_title)
        details_page.click_pay_with_paypal()
        Assert.contains("Log in to your PayPal account to complete this purchase.", details_page.paypal_login_message)