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
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
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
import pytest
from unittestzero import Assert

from selenium.webdriver.common.by import By

from pages.page import Page
from pages.base import Base


class ExtensionsHome(Base):

    _page_title = 'Featured Extensions :: Add-ons for Firefox'
    _extensions_locator = (By.CSS_SELECTOR, "div.items div.item")
    _last_page_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(4)")
    _first_page_link_locator = (By.CSS_SELECTOR, ".paginator .rel > a:nth-child(1)")
    _top_rated_locator = (By.CSS_SELECTOR, "#sorter > ul > li:nth-child(3)")
    _free_addon_button_text_locator = (By.LINK_TEXT, "Add to Firefox")
    _free_extensions_list_locator = (By.CSS_SELECTOR, "div.items > div[class='item addon']")
    #_free_extensions_install_button_locator = (By.CSS_SELECTOR, " div.action > div[class='install-shell'] > div[class='install lite clickHijack']")

    @property
    def extensions(self):
        return [Extension(self.testsetup, element)
                for element in self.selenium.find_elements(*self._extensions_locator)]
                
    @property
    def compatible_extensions(self):
        return self.selenium.find_elements(By.CSS_SELECTOR, "div.items > div[class='item addon']")
                #for element in self.selenium.find_elements_by_css_selector("div.items > div[class='item addon']")]

    def go_to_last_page(self):
        self.selenium.find_element(*self._last_page_link_locator).click()

    def go_to_first_page(self):
        self.selenium.find_element(*self._first_page_link_locator).click()

    def click_top_rated(self):
        self.selenium.find_element(*self._top_rated_locator).click()

    @property
    def unreviewed_free_extension(self):
        self.click_top_rated()
        self.go_to_last_page()
        #look for first extension with "Not yet rated" and button != purchase
        try:
            for extension_list_item in self.compatible_extensions:
                #how will the list item maintain scope for this if statement?
                if self.extension_is_free && not self.extension_is_rated: 
                    return Extension(self.testsetup, self.compatible_extensions)
        except IndexError:
            print "There were no unrated, free apps on the last page of extensions."
        #return Extension(self.testsetup, self.compatible_extensions[-1])

    @property
    def extension_is_free(self):
        pass

    @property
    def extension_is_rated(self):
        pass

class Extension(Page):
        _name_locator = (By.CSS_SELECTOR, "div.items > div[class='item addon'] > div.info > h3 a")
        _button_text_locator = (By.CSS_SELECTOR, "div.items > div[class='item addon']  div.action > div[class='install-shell'] > div[class='install lite clickHijack']")

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        def button_text(self):
            return self._root_element.find_element(*self_button_text_locator).text

        def click(self):
            self._root_element.find_element(*self._name_locator).click()
            from pages.details import Details
            return Details(self.testsetup)

