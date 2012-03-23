#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.home import Home
from pages.desktop.details import Details


class TestPaypal:
    """
    This test only works with Firefox 7.
    Until Selenium issue http://code.google.com/p/selenium/issues/detail?id=2067 is fixed.
    """

    addon_name = 'Adblock Plus'

    @pytest.mark.login
    def test_that_user_can_contribute_to_an_addon(self, mozwebqa):
        """Test that checks the Contribute button for an addon using PayPal."""

        addon_page = Home(mozwebqa)

        addon_page.login('browserID')
        Assert.true(addon_page.is_the_current_page)
        Assert.true(addon_page.header.is_user_logged_in)

        addon_page = Details(mozwebqa, self.addon_name)

        contribution_snippet = addon_page.click_contribute_button()
        paypal_frame = contribution_snippet.click_make_contribution_button()
        Assert.true(addon_page.is_paypal_login_dialog_visible)

        payment_popup = paypal_frame.login_to_paypal(user="paypal")
        Assert.true(payment_popup.is_user_logged_into_paypal)
        payment_popup.click_pay()
        Assert.true(payment_popup.is_payment_successful)
        payment_popup.close_paypal_popup()
        Assert.true(addon_page.is_the_current_page)

    def test_that_user_can_make_a_contribution_without_logging_into_amo(self, mozwebqa):
        """Test that checks if the user is able to make a contribution without logging in to AMO."""
        addon_page = Details(mozwebqa, 'Adblock Plus')
        Assert.false(addon_page.header.is_user_logged_in)

        contribution_snippet = addon_page.click_contribute_button()
        paypal_frame = contribution_snippet.click_make_contribution_button()
        Assert.true(addon_page.is_paypal_login_dialog_visible)

        payment_popup = paypal_frame.login_to_paypal(user="paypal")
        Assert.true(payment_popup.is_user_logged_into_paypal)
        payment_popup.click_pay()
        Assert.true(payment_popup.is_payment_successful)
        payment_popup.close_paypal_popup()
        Assert.true(addon_page.is_the_current_page)
