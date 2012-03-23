#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.desktop.home import Home


class HeaderMenu:

    def __init__(self, name, items):
        self.name = name
        self.items = items

    @property
    def name(self):
        return self.name

    @property
    def items(self):
        return self.items


class TestHome:

    expected_header_menus = [
        HeaderMenu('EXTENSIONS', [
            "Featured", "Most Popular", "Top Rated", "Alerts & Updates", "Appearance", "Bookmarks",
            "Download Management", "Feeds, News & Blogging", "Games & Entertainment",
            "Language Support", "Photos, Music & Videos", "Privacy & Security", "Shopping",
            "Social & Communication", "Tabs", "Web Development", "Other"]),
        HeaderMenu('PERSONAS', [
            "Most Popular", "Top Rated", "Newest", "Abstract", "Causes", "Fashion", "Film and TV",
            "Firefox", "Foxkeh", "Holiday", "Music", "Nature", "Other", "Scenery", "Seasonal",
            "Solid", "Sports", "Websites"]),
        HeaderMenu('THEMES', [
            "Most Popular", "Top Rated", "Newest", "Animals", "Compact", "Large", "Miscellaneous",
            "Modern", "Nature", "OS Integration", "Retro", "Sports"]),
        HeaderMenu('COLLECTIONS', [
            "Featured", "Most Followers", "Newest", "Collections I've Made",
            "Collections I'm Following", "My Favorite Add-ons"]),
        HeaderMenu(u'MORE\u2026', [
            "Add-ons for Mobile", "Dictionaries & Language Packs", "Search Tools", "Developer Hub"])]

    @pytest.mark.nondestructive
    def test_that_checks_the_most_popular_section_exists(self, mozwebqa):
        """
        Test for Litmus 25807.
        https://litmus.mozilla.org/show_test.cgi?id=25807
        """
        home_page = Home(mozwebqa)
        Assert.contains('MOST POPULAR', home_page.most_popular_list_heading)
        Assert.equal(home_page.most_popular_count, 10)

    @pytest.mark.nondestructive
    def test_that_clicking_on_addon_name_loads_details_page(self, mozwebqa):
        """
        Test for Litmus 25812.
        https://litmus.mozilla.org/show_test.cgi?id=25812
        """
        home_page = Home(mozwebqa)
        details_page = home_page.click_on_first_addon()
        Assert.true(details_page.is_the_current_page)

    @pytest.mark.nondestructive
    def test_that_featured_personas_exist_on_the_home(self, mozwebqa):
        """
        Test for Litmus29698.
        https://litmus.mozilla.org/show_test.cgi?id=29698
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.featured_personas_title, u'Featured Personas See all \xbb', 'Featured Personas region title doesn\'t match')
        Assert.less_equal(home_page.featured_personas_count, 6)

    @pytest.mark.nondestructive
    def test_that_clicking_see_all_personas_link_works(self, mozwebqa):
        """
        Test for Litmus 29699.
        https://litmus.mozilla.org/show_test.cgi?id=29699
        """
        home_page = Home(mozwebqa)
        featured_persona_page = home_page.click_featured_personas_see_all_link()

        Assert.true(featured_persona_page.is_the_current_page)
        Assert.equal(featured_persona_page.persona_header, 'Personas')

    @pytest.mark.nondestructive
    def test_that_extensions_link_loads_extensions_page(self, mozwebqa):
        """
        Test for Litmus 25746.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25746
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.header.site_navigation_menu("EXTENSIONS").click()
        Assert.true(extensions_page.is_the_current_page)

    @pytest.mark.nondestructive
    def test_that_most_popular_section_is_ordered_by_users(self, mozwebqa):
        """
        Test for Litmus 25808.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25808
        """
        home_page = Home(mozwebqa)

        most_popular_items = home_page.most_popular_items
        Assert.is_sorted_descending([i.users_number for i in most_popular_items])

    @pytest.mark.nondestructive
    def test_that_featured_collections_exist_on_the_home(self, mozwebqa):
        """
        Test for Litmus 25805.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25805
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.featured_collections_title, u'Featured Collections See all \xbb', 'Featured Collection region title doesn\'t match')
        Assert.equal(home_page.featured_collections_count, 4)

    @pytest.mark.nondestructive
    def test_that_featured_extensions_exist_on_the_home(self, mozwebqa):
        """
        Test for Litmus 25800.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25800
        """
        home_page = Home(mozwebqa)
        Assert.equal(home_page.featured_extensions_title, 'Featured Extensions', 'Featured Extensions region title doesn\'t match')
        Assert.equal(home_page.featured_extensions_see_all, u'See all \xbb', 'Featured Extensions region see all link is not correct')
        Assert.equal(home_page.featured_extensions_count, 6)

    @pytest.mark.nondestructive
    def test_that_clicking_see_all_collections_link_works(self, mozwebqa):
        """
        Test for Litmus 25806.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25806
        """
        home_page = Home(mozwebqa)
        featured_collection_page = home_page.click_featured_collections_see_all_link()
        Assert.true(featured_collection_page.is_the_current_page)
        Assert.true(featured_collection_page.get_url_current_page().endswith('/collections/?sort=featured'))

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_items_menu_fly_out_while_hovering(self, mozwebqa):
        """
        Test for Litmus 25754.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25754
        """
        #I've adapted the test to check open/closed for all menu items
        home_page = Home(mozwebqa)

        for menu in self.expected_header_menus:
            menu_item = home_page.header.site_navigation_menu(menu.name)
            menu_item.hover()
            Assert.true(menu_item.is_menu_dropdown_visible)
            home_page.hover_over_addons_home_title()
            Assert.false(menu_item.is_menu_dropdown_visible)

    def test_that_clicking_top_rated_shows_addons_sorted_by_rating(self, mozwebqa):
        """
        Test for Litmus 25791.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25791
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('top_rated')

        Assert.contains('sort=rating', extensions_page.get_url_current_page())
        Assert.equal('Top Rated', extensions_page.default_selected_tab)

    @pytest.mark.nondestructive
    def test_that_clicking_most_popular_shows_addons_sorted_by_users(self, mozwebqa):
        """
        Test for Litmus 25790.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25790
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('popular')

        Assert.contains('sort=users', extensions_page.get_url_current_page())
        Assert.equal('Most Users', extensions_page.default_selected_tab)

    @pytest.mark.nondestructive
    def test_that_clicking_featured_shows_addons_sorted_by_featured(self, mozwebqa):
        """
        Test for Litmus 25790.
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25790
        """
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('featured')

        Assert.contains('sort=featured', extensions_page.get_url_current_page())
        Assert.equal('Featured', extensions_page.default_selected_tab)

    @pytest.mark.nondestructive
    @pytest.mark.litmus(25744)
    def test_header_site_navigation_menus_are_correct(self, mozwebqa):
        home_page = Home(mozwebqa)

        # compile lists of the expected and actual top level navigation items
        expected_navigation_menu = [menu.name for menu in self.expected_header_menus]
        actual_navigation_menus = [actual_menu.name for actual_menu in home_page.header.site_navigation_menus]

        Assert.equal(expected_navigation_menu, actual_navigation_menus)

    @pytest.mark.native
    @pytest.mark.nondestructive
    @pytest.mark.litmus([25745, 25747, 25749, 25751, 25754, 25756, 25758, 25760, 25763, 25764])
    def test_the_name_of_each_site_navigation_menu_in_the_header(self, mozwebqa):
        home_page = Home(mozwebqa)

        # loop through each expected menu and collect a list of the items in the menu
        # and then assert that they exist in the actual menu on the page
        for menu in self.expected_header_menus:
            expected_menu_items = menu.items
            actual_menu_items = [menu_items.name for menu_items in home_page.header.site_navigation_menu(menu.name).items]

            Assert.equal(expected_menu_items, actual_menu_items)

    @pytest.mark.nondestructive
    @pytest.mark.litmus([25747, 25751, 25756, 25760, 25764])
    def test_top_three_items_in_each_site_navigation_menu_are_featured(self, mozwebqa):
        home_page = Home(mozwebqa)

        # loop through each actual top level menu
        for actual_menu in home_page.header.site_navigation_menus:
            # 'more' navigation_menu has no featured items so we have a different assertion
            if actual_menu.name == u"MORE\u2026":
                # loop through each of the items in the top level menu and check is_featured property
                [Assert.false(item.is_featured) for item in actual_menu.items]
            else:
                # first 3 are featured, the others are not
                [Assert.true(item.is_featured) for item in actual_menu.items[:3]]
                [Assert.false(item.is_featured) for item in actual_menu.items[3:]]
