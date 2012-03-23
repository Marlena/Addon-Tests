#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.desktop.base import Base
from pages.page import Page


class Themes(Base):

    _sort_by_name_locator = (By.CSS_SELECTOR, 'li.extras > ul > li:nth-child(1) > a')
    _sort_by_updated_locator = (By.CSS_SELECTOR, 'li.extras > ul > li:nth-child(4) > a')
    _sort_by_created_locator = (By.CSS_SELECTOR, 'div#sorter > ul > li:nth-child(3) > a')
    _sort_by_popular_locator = (By.CSS_SELECTOR, 'li.extras > ul > li:nth-child(3) > a')
    _sort_by_rating_locator = (By.CSS_SELECTOR, 'div#sorter > ul > li:nth-child(2) > a')
    _selected_sort_by_locator = (By.CSS_SELECTOR, '#sorter > ul > li.selected a')
    _hover_more_locator = (By.CSS_SELECTOR, 'li.extras > a')
    _addons_root_locator = (By.CSS_SELECTOR, '.listing-grid li')
    _addon_name_locator = (By.CSS_SELECTOR, 'h3')
    _addons_metadata_locator = (By.CSS_SELECTOR, '.vital .updated')
    _addons_download_locator = (By.CSS_SELECTOR, '.downloads.adu')
    _addons_rating_locator = (By.CSS_SELECTOR, 'span span')
    _category_locator = (By.CSS_SELECTOR, '#c-30 > a')
    _categories_locator = (By.CSS_SELECTOR, '#side-categories li')
    _category_link_locator = (By.CSS_SELECTOR, _categories_locator[1] + ':nth-of-type(%s) a')
    _next_link_locator = (By.CSS_SELECTOR, '.paginator .rel > a:nth-child(3)')
    _previous_link_locator = (By.CSS_SELECTOR, '.paginator .rel > a:nth-child(2)')
    _last_page_link_locator = (By.CSS_SELECTOR, '.rel > a:nth-child(4)')
    _explore_filter_links_locators = (By.CSS_SELECTOR, '#side-explore a')

    @property
    def _addons_root_element(self):
        return self.selenium.find_element(*self._addons_root_locator)

    def click_sort_by(self, type_):
        click_target = self.selenium.find_element(*getattr(self, "_sort_by_%s_locator" % type_))
        hover_element = self.selenium.find_element(*self._hover_more_locator)
        footer = self.selenium.find_element(*self._footer_locator)
        ActionChains(self.selenium).\
            move_to_element(footer).\
            move_to_element(hover_element).\
            move_to_element(click_target).\
            click().perform()

    @property
    def sorted_by(self):
        return self.selenium.find_element(*self._selected_sort_by_locator).text

    @property
    def selected_explore_filter(self):
        for link in self.selenium.find_elements(*self._explore_filter_links_locators):
            selected = link.value_of_css_property('font-weight')
            if selected == 'bold' or int(selected) > 400:
                return link.text

    def click_on_first_addon(self):
        self._addons_root_element.find_element(*self._addon_name_locator).click()
        return Theme(self.testsetup)

    def click_on_first_category(self):
        self.selenium.find_element(*self._category_locator).click()
        return ThemesCategory(self.testsetup)

    def get_category(self, lookup):
        return self.selenium.find_element(self._category_link_locator[0],
                                          self._category_link_locator[1] % lookup).text

    @property
    def themes_category(self):
        return self.selenium.find_element(*self._category_locator).text

    @property
    def categories_count(self):
        return len(self.selenium.find_elements(*self._categories_locator))

    @property
    def get_all_categories(self):
        return [element.text for element in self.selenium.find_elements(*self._categories_locator)]

    @property
    def addon_names(self):
        addon_name = []
        for addon in self._addons_root_element.find_elements(*self._addon_name_locator):
            ActionChains(self.selenium).move_to_element(addon).perform()
            addon_name.append(addon.text)
        return addon_name

    def addon_name(self, lookup):
        return self.selenium.find_element(By.CSS_SELECTOR,
                                          "%s:nth-of-type(%s) h3" % (self._addons_root_locator[1], lookup)).text

    @property
    def addon_count(self):
        return len(self._addons_root_element.find_elements(*self._addon_name_locator))

    @property
    def addon_updated_dates(self):
        return self._extract_iso_dates("Updated %B %d, %Y", *self._addons_metadata_locator)

    @property
    def addon_created_dates(self):
        return self._extract_iso_dates("Added %B %d, %Y", *self._addons_metadata_locator)

    @property
    def addon_download_number(self):
        pattern = "(\d+(?:[,]\d+)*) weekly downloads"
        downloads = self._extract_integers(pattern, *self._addons_download_locator)
        return downloads

    @property
    def addon_rating(self):
        pattern = "(\d)"
        ratings = self._extract_integers(pattern, *self._addons_rating_locator)
        return ratings

    @property
    def themes(self):
        return [self.Theme(self.testsetup, theme)for theme in self.selenium.find_elements(*self._addons_root_locator)]

    class Theme(Page):

        _not_compatible_locator = (By.CSS_SELECTOR, "div.hovercard > span.notavail")
        _hovercard_locator = (By.CSS_SELECTOR, "div.hovercard")

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def is_incompatible(self):
            return 'incompatible' in self._root_element.find_element(*self._hovercard_locator).get_attribute('class')

        @property
        def not_compatible_flag_text(self):
            return self._root_element.find_element(*self._not_compatible_locator).text

        @property
        def is_incompatible_flag_present(self):
            from selenium.common.exceptions import NoSuchElementException
            try:
                self._root_element.find_element(*self._not_compatible_locator)
                return True
            except NoSuchElementException:
                return False


class Theme(Base):

    _addon_title = (By.CSS_SELECTOR, "h1.addon")

    @property
    def addon_title(self):
        return self.selenium.find_element(*self._addon_title).text


class ThemesCategory(Base):

    _title_locator = (By.CSS_SELECTOR, "section.primary > h1")
    _breadcrumb_locator = (By.CSS_SELECTOR, "#breadcrumbs > ol")

    @property
    def title(self):
        return self.selenium.find_element(*self._title_locator).text
