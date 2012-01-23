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
# Contributor(s): David Burns
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Bebe <florin.strugariu@softvision.ro>
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

from pages.home import Home

xfail = pytest.mark.xfail
nondestructive = pytest.mark.nondestructive


class TestSearch:

    @nondestructive
    def test_that_entering_a_long_string_returns_no_results(self, mozwebqa):
        """ Litmus 4856
            https://litmus.mozilla.org/show_test.cgi?id=4856 """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('a' * 255)

        Assert.true(search_page.is_no_results_present)
        Assert.equal('No results found.', search_page.no_results_text)

        Assert.true('0 matching results' in search_page.number_of_results_text)

    @nondestructive
    def test_that_searching_with_substrings_returns_results(self, mozwebqa):
        """ Litmus 9561
            https://litmus.mozilla.org/show_test.cgi?id=9561 """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('marble')

        Assert.false(search_page.is_no_results_present, 'No results were found')

        results_text_summary = search_page.number_of_results_text
        Assert.not_equal(u'0 matching results', results_text_summary)

        Assert.true(int(results_text_summary.split()[0]) > 1)

    @nondestructive
    def test_that_blank_search_returns_results(self, mozwebqa):
        """ Litmus 11759
            https://litmus.mozilla.org/show_test.cgi?id=11759 """
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for("")

        Assert.false(search_page.is_no_results_present)
        Assert.greater(search_page.result_count, 0)

    @nondestructive
    def test_that_page_with_search_results_has_correct_title(self, mozwebqa):
        """ Litmus 17338
            https://litmus.mozilla.org/show_test.cgi?id=17338 """
        home_page = Home(mozwebqa)
        search_keyword = 'Search term'
        search_page = home_page.header.search_for(search_keyword)

        expected_title = '%s :: Search :: Apps Developer Preview' % search_keyword
        Assert.equal(expected_title, search_page.page_title)

    @nondestructive
    def test_that_searching_for_fire_returns_firebug(self, mozwebqa):
        """Litmus 15314
        https://litmus.mozilla.org/show_test.cgi?id=15314"""
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('fire')

        Assert.equal(search_page.result(0).name, 'Firebug')

    @nondestructive
    def test_that_searching_for_marble_returns_results_with_cool_in_their_name_description(self, mozwebqa):
        """Litmus 17353
        https://litmus.mozilla.org/show_test.cgi?id=17353"""
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for('Marble')

        for i in range(10):
            Assert.contains('marble', search_page.result(i).text.lower())

    #:TODO To be merged into a layout test
    @nondestructive
    def test_the_search_field_placeholder(self, mozwebqa):
        """Litmus 4826
        https://litmus.mozilla.org/show_test.cgi?id=4826"""
        home_page = Home(mozwebqa)
        Assert.equal(home_page.header.search_field_placeholder, 'search for apps')

    @nondestructive
    def test_that_searching_with_numerals_returns_results(self, mozwebqa):
        """Litmus 17347
        https://litmus.mozilla.org/show_test.cgi?id=17347"""
        search_page = Home(mozwebqa).header.search_for('1')

        Assert.greater(search_page.result_count, 0)
        Assert.true(int(search_page.number_of_results_text.split()[0]) > 0)
