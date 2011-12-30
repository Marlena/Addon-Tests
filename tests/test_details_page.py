#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Teodosia Pop <teodosia.pop@softvision.ro>
#                 Bebe <florin.strugariu@softvision.ro>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Alin Trif <alin.trif@softvision.ro>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****


import re
import pytest

from unittestzero import Assert

from pages.details import Details
from pages.extensions import ExtensionsHome
from pages.home import Home

nondestructive = pytest.mark.nondestructive


class TestDetails:

    @nondestructive
    def test_that_register_login_link_is_present_in_addon_details_page(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.register_link, "Log in / Register", "Login / Register text does not match the expected one")

    @nondestructive
    def test_that_dropdown_menu_is_present_after_click_on_other_apps(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.other_apps, "Other Applications")
        #TODO: Fix when the hover event works
        #Assert.true(details_page.is_other_apps_dropdown_menu_visible

    @nondestructive
    def test_that_addon_name_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        # check that the name is not empty
        Assert.not_none(details_page.title, "")

    @nondestructive
    def test_that_summary_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        # check that the summary is not empty
        Assert.not_none(re.match('(\w+\s*){3,}', details_page.summary))

    @nondestructive
    def test_that_about_this_addon_is_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.about_addon, "About this App")
        Assert.not_none(re.match('(\w+\s*){3,}', details_page.description))

    @nondestructive
    def test_that_reviews_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.review_title, "Reviews")
        Assert.true(details_page.has_reviews)
        Assert.not_none(re.search('(\w+\s*){1,}', details_page.review_details))

    @nondestructive
    def test_that_in_often_used_with_addons_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.equal(details_page.often_used_with_header, u"Often used with\u2026")
        Assert.true(details_page.is_often_used_with_list_visible)

    @nondestructive
    def test_that_tags_are_displayed(self, mozwebqa):
        """ Test for Litmus 9890"""
        details_page = Details(mozwebqa, "Firebug")
        Assert.true(details_page.are_tags_visible)

    @nondestructive
    def test_that_external_link_leads_to_addon_website(self, mozwebqa):
        """ Litmus 11809
            https://litmus.mozilla.org/show_test.cgi?id=11809 """
        # Step 1 - Open AMO Home
        # Step 2 - Open Adblock Plus details page
        details_page = Details(mozwebqa, 'Adblock Plus')
        website_link = details_page.website
        Assert.true(website_link != '')
        # Step 3 - Follow external website link
        details_page.click_website_link()
        Assert.true(website_link in details_page.get_url_current_page())

    @nondestructive
    def test_other_addons_label_when_there_is_only_one_author(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926
        """
        addon_with_one_authors = 'F1 by Mozilla Labs'
        detail_page = Details(mozwebqa, addon_with_one_authors)

        Assert.equal(len(detail_page.authors), 1)
        Assert.equal(detail_page.other_addons_by_authors_text, "Other add-ons by %s" % detail_page.authors[0])

    @nondestructive
    def test_navigating_to_other_addons(self, mozwebqa):
        """
        Litmus 11926
        https://litmus.mozilla.org/show_test.cgi?id=11926"""
        detail_page = Details(mozwebqa, 'firebug')

        for i in range(0, len(detail_page.other_addons)):
            name = detail_page.other_addons[i].name
            detail_page.other_addons[i].click_addon_link()
            Assert.contains(name, detail_page.title)
            Details(mozwebqa, 'firebug')

    @nondestructive
    def test_that_review_usernames_are_clickable(self, mozwebqa):
        """
        Litmus 4842
        https://litmus.mozilla.org/show_test.cgi?id=4842
        """
        addon_name = 'firebug'
        detail_page = Details(mozwebqa, addon_name)

        for i in range(0, len(detail_page.reviews)):
            username = detail_page.reviews[i].username
            amo_user_page = detail_page.reviews[i].click_username()
            Assert.equal(username, amo_user_page.username)
            Details(mozwebqa, addon_name)

    @nondestructive
    def test_that_details_page_has_breadcrumb(self, mozwebqa):
        """
        Litmus 11922
        https://litmus.mozilla.org/show_test.cgi?id=11922
        """
        detail_page = Details(mozwebqa, 'firebug')
        Assert.equal(detail_page.breadcrumb, 'Apps Marketplace\nApps Firebug')

    @nondestructive
    def test_that_breadcrumb_links_in_details_page_work(self, mozwebqa):
        """
        Litmus 11923
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=11923
        """
        home_page = Home(mozwebqa)
        detail_page = Details(mozwebqa, 'firebug')

        Assert.equal(detail_page.breadcrumbs[0].name, 'Apps Marketplace')
        link = detail_page.breadcrumbs[0].link_value
        detail_page.breadcrumbs[0].click_breadcrumb()

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.get_url_current_page().endswith(link))

    @nondestructive
    def test_that_add_a_review_button_works(self, mozwebqa):
        """
        Litmus 25729
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25729
        """
        details_page = Details(mozwebqa, 'marble-run-12')
        review_box = details_page.click_to_write_review()
        Assert.true(review_box.is_review_box_visible)