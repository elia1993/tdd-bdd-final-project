######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
import time
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = 'product_'


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.driver.get(context.base_url)


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message"""
    assert message in context.driver.title


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    """Check that text is not on the page"""
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert text_string not in element.text


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set a field to some text"""
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Select from a dropdown"""
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    select_element = Select(context.driver.find_element(By.ID, element_id))
    select_element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Check dropdown selected value"""
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    select_element = Select(context.driver.find_element(By.ID, element_id))
    assert select_element.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Check that a field is empty"""
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute('value') == ''


@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy the contents of a field"""
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste into a field"""
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)


@when('I press the "{button}" button')
def step_impl(context, button):
    """Press a button by ID"""
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()
    time.sleep(1)


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Verify a flash message"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert found


@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """Check that a field contains some text"""
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    assert found


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Change the value of a field"""
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


@then('I should see "{name}" in the results')
def step_impl(context, name):
    """Verify that a name appears in the results"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    assert found


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    """Verify that a name does not appear in the results"""
    element = context.driver.find_element(By.ID, 'search_results')
    assert name not in element.text