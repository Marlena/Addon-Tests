#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from datetime import datetime
from unittestzero import Assert

from pages.desktop.home import Home
from pages.desktop.details import Details
from pages.desktop.addons_site import ViewReviews


class TestReviews:

    @pytest.mark.nondestructive
    def test_that_all_reviews_hyperlink_works(self, mozwebqa):
        """
        Test for Litmus 4843.
        https://litmus.mozilla.org/show_test.cgi?id=4843
        """
        #Open details page for MemChaser
        details_page = Details(mozwebqa, 'MemChaser')
        Assert.true(details_page.has_reviews)

        details_page.click_all_reviews_link()
        Assert.equal(details_page.review_count, 20)

        #Go to the last page and check that the next button is not present
        details_page.paginator.click_last_page()
        Assert.true(details_page.paginator.is_next_page_disabled)

        #Go one page back, check that it has 20 reviews
        #that the page number decreases and that the next link is visible
        page_number = details_page.paginator.page_number
        details_page.paginator.click_prev_page()
        Assert.false(details_page.paginator.is_next_page_disabled)
        Assert.equal(details_page.review_count, 20)
        Assert.equal(details_page.paginator.page_number, page_number - 1)

        #Go to the first page and check that the prev button is not present
        details_page.paginator.click_first_page()
        Assert.true(details_page.paginator.is_prev_page_disabled)

        #Go one page forward, check that it has 20 reviews,
        #that the page number increases and that the prev link is visible
        page_number = details_page.paginator.page_number
        details_page.paginator.click_next_page()
        Assert.false(details_page.paginator.is_prev_page_disabled)
        Assert.equal(details_page.review_count, 20)
        Assert.equal(details_page.paginator.page_number, page_number + 1)

    @pytest.mark.native
    @pytest.mark.login
    def test_that_new_review_is_saved(self, mozwebqa):
        """
        Test for Litmus 22921.
        https://litmus.mozilla.org/show_test.cgi?id=22921
        """
        # Step 1 - Login into AMO
        home_page = Home(mozwebqa)
        home_page.login("browserID")
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        # Step 2 - Load any addon detail page
        details_page = Details(mozwebqa, 'Memchaser')

        # Step 3 - Click on "Write review" button
        write_review_block = details_page.click_to_write_review()

        # Step 4 - Write a review
        body = 'Automatic addon review by Selenium tests %s' % datetime.now()
        write_review_block.enter_review_with_text(body)
        write_review_block.set_review_rating(1)
        review_page = write_review_block.click_to_save_review()

        # Step 5 - Assert review
        review = review_page.reviews[0]
        Assert.equal(review.rating, 1)
        Assert.equal(review.author, mozwebqa.credentials['default']['name'])
        date = datetime.now().strftime("%B %d, %Y")
        # there are no leading zero-signs on day so we need to remove them too
        date = date.replace(' 0', ' ')
        Assert.equal(review.date, date)
        Assert.equal(review.text, body)

        review.delete()

        details_page = Details(mozwebqa, 'Memchaser')
        review_page = details_page.click_all_reviews_link()

        for review in review_page.reviews:
            Assert.false(body in review.text)

    @pytest.mark.login
    @pytest.mark.parametrize(('star_rating'), [(1), (2), (3), (4), (5)])
    @pytest.mark.native
    def test_that_rating_counter_increments_on_giving_star_rating(self, mozwebqa, star_rating):
        """
        Test for Litmus 22916, 22917, 22918, 22919, 22920.
        """
        home_page = Home(mozwebqa)
        home_page.login()
        Assert.true(home_page.header.is_user_logged_in)

        #Go to add-ons listing page sorted by rating
        extensions_home_page = home_page.click_to_explore('Top Rated')

        #Pick an addon with no reviews
        extensions_home_page.paginator.click_last_page()
        addon = extensions_home_page.extensions_with_no_reviews[-1]
        details_page_to_be_reviewed = addon.click()
        original_number_of_reviews = details_page_to_be_reviewed.total_number_of_reviews_for_all_ratings

        #Click on the "Write review" button
        write_review_block = details_page_to_be_reviewed.click_to_write_review()

        #Add review with star rating
        review_text = 'Automatic addon review by Selenium tests'
        write_review_block.enter_review_with_text(review_text)
        write_review_block.set_review_rating(star_rating)
        view_reviews_page = write_review_block.click_to_save_review()
        reviewed_details_page = view_reviews_page.navigate_back_to_details_page_with_review(mozwebqa)

        #Since the review has been created with a star_rating,
        #has the number of ratings for the addon increased by 1?
        new_number_of_reviews = reviewed_details_page.total_number_of_reviews_for_all_ratings
        Assert.equal(new_number_of_reviews, (original_number_of_reviews + 1), str("Addon reviewed was: " + reviewed_details_page.title + "\nStar_rating was: " + str(star_rating)))