import hashlib
import logging
import re
import smtplib
from datetime import time, datetime
import datetime
import urllib.parse
from collections import OrderedDict
from pprint import pprint
from urllib import error
from lxml import html

import bcrypt
import requests
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from Geoportal.decorator import check_browser
from Geoportal.geoportalObjects import GeoportalJsonResponse, GeoportalContext
from Geoportal.settings import DEFAULT_GUI, HOSTNAME, HTTP_OR_SSL, INTERNAL_SSL, \
    SESSION_NAME, PROJECT_DIR, MULTILINGUAL, LANGUAGE_CODE, DEFAULT_FROM_EMAIL, GOOGLE_RECAPTCHA_SECRET_KEY, \
    USE_RECAPTCHA, GOOGLE_RECAPTCHA_PUBLIC_KEY, DEFAULT_TO_EMAIL, MOBILE_WMC_ID
from Geoportal.utils import utils, php_session_data, mbConfReader
from searchCatalogue.utils.url_conf import URL_INSPIRE_DOC
from searchCatalogue.settings import PROXIES
from useroperations.settings import LISTED_VIEW_AS_DEFAULT, ORDER_BY_DEFAULT, INSPIRE_CATEGORIES, ISO_CATEGORIES
from useroperations.utils import useroperations_helper
from .forms import RegistrationForm, LoginForm, PasswordResetForm, ChangeProfileForm, DeleteProfileForm, FeedbackForm
from .models import MbUser, MbGroup, MbUserMbGroup, MbRole, GuiMbUser, MbProxyLog, Wfs, Wms

logger = logging.getLogger(__name__)



def prioritize_top_news(parsed_data):
    """
    Prioritizes "topNews" items based on their repair start dates and durations.

    This function calculates the repair start date for each "topNews" item by adding
    its duration to the specified date. It then sorts the items based on the number
    of days until the repair start date, in ascending order. Items with repair dates
    that have already passed are filtered out.

    Additionally, if multiple "topNews" items have the same title and date, the latest entry
    will be prioritized at the top of the list.

    Args:
        parsed_data (list of dict): A list of "topNews" items, each represented as a dictionary
            with keys "title," "date," "duration," "teaser," and "article_body."

    Returns:
        list of dict: A sorted and filtered list of "topNews" items, prioritized by their repair dates.

    Edited by: Deepak Parajuli
    """
    
    # Get today's date
    today = datetime.date.today()

    # Define a custom sorting function
    def custom_sort(item):
        # Parse the date into a format that can be compared
        date_parts = item["date"].split(".")
        parsed_date = datetime.date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))

        # Calculate the repair start date based on duration
        if item["duration"]:
            repair_start_date = parsed_date + datetime.timedelta(days=int(item["duration"]))
        else:
            repair_start_date = parsed_date

        # Calculate the difference in days between today and the repair start date
        days_until_repair = (repair_start_date - today).days

        # Sort by days until repair (ascending)
        return days_until_repair

    # Sort the parsed data using the custom sorting function
    try:
        sorted_data = sorted(parsed_data, key=custom_sort)

        # Filter out "topNews" items with repair dates that have already passed
        sorted_data = [item for item in sorted_data if custom_sort(item) >= 0]
        return sorted_data
    except:
        pass

    


def parse_wiki_data():
    """
    Parse the "Meldungen" page on the wiki and return the prioritized top news, along with a URL
    to see more details if available.

    Args:
        request: The HTTP request object (not explicitly used in this function).

    Returns:
        tuple: A tuple containing two elements:
            - A list of prioritized top news items, each represented as a dictionary with keys
              "title," "date," "duration," "teaser," and "article_body."
            - A URL to see more details about the top news on the wiki page, or an empty string if
              there are no top news items.

    This function performs the following steps:
    1. Constructs the URL for the Wikimedia API endpoint.
    2. Sends a request to the API to parse the "Meldungen" page.
    3. Parses the JSON response to extract the HTML content.
    4. Extracts information from HTML elements within "topNews" divs, including title, date,
       duration, teaser, and article body.
    5. Prioritizes the top news items based on repair start dates and durations.
    6. Generates a URL to see more details about the top news item, adapted for MediaWiki encoding.
    7. Returns the prioritized top news and the see more URL.
    Edited by: Deepak Parajuli
    """
    # Define the URL of your Wikimedia API endpoint
    api_url = HTTP_OR_SSL + HOSTNAME + "/mediawiki/api.php"

    # Define parameters for the API request to parse the "Meldungen" page
    params = {
        "action": "parse",
        "format": "json",
        "page": "Meldungen",  
        "formatversion": 2
    }

    response = requests.get(api_url, params=params)
    parsed_data = []

    # Check if the API request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        parsed_content = data["parse"]["text"]

        # Parse the HTML content (in 'parsed_content') and create an HTML tree structure for further processing.
        html_tree = html.fromstring(parsed_content)
        
        # Find all div elements with class="topNews" 
        top_news_elements = html_tree.cssselect("div.topNews")
        
        for top_news in top_news_elements:
            #delete the codes below after the test is successful and find if I could send anything in except (TODO)
            # Attempt to find specific HTML elements with certain attributes or classes inside the 'top_news' element(s).
            # If found, assign them to respective variables; otherwise, assign 'None'.
            # title_element = top_news.cssselect("h2.topNewsTitle")[0] if top_news.cssselect("h2.topNewsTitle") else None 
            # date_element = top_news.cssselect("span.topNewsDate strong")[0] if top_news.cssselect("span.topNewsDate strong") else None 
            # duration_element = top_news.cssselect("span.hiddenDuration")[0] if top_news.cssselect("span.hiddenDuration") else None 
            # teaser_element = top_news.cssselect("p.teaser")[0] if top_news.cssselect("p.teaser") else None
            # article_body_element = top_news.cssselect("p.articleBody")[0] if top_news.cssselect("p.articleBody") else None 

            try:
                title_element = top_news.cssselect("h2.topNewsTitle")[0]
            except IndexError:
                title_element = None

            try:
                date_element = top_news.cssselect("span.topNewsDate strong")[0]
            except IndexError:
                date_element = None

            try:
                duration_element = top_news.cssselect("span.hiddenDuration")[0]
            except IndexError:
                duration_element = None

            try:
                teaser_element = top_news.cssselect("p.teaser")[0]
            except IndexError:
                teaser_element = None

            try:
                article_body_element = top_news.cssselect("p.articleBody")[0]
            except IndexError:
                article_body_element = None


            #delete this after the test is successful (TODO)
            #check if the element exists
            # title = title_element.text_content().strip() if title_element is not None else ""
            # date = date_element.text.strip() if date_element is not None else ""
            # duration = duration_element.text.strip() if duration_element is not None else ""
            # teaser = teaser_element.text_content().strip() if teaser_element is not None else ""
            # article_body = article_body_element.text_content().strip() if article_body_element is not None else ""

            try:
                title = title_element.text_content().strip()
            except AttributeError:
                title = ""

            try:
                date = date_element.text.strip()
            except AttributeError:
                date = None
                continue

           

            try:
                duration = duration_element.text.strip()
            except AttributeError:
                duration = ""

            try:
                teaser = teaser_element.text_content().strip()
            except AttributeError:
                teaser = ""

            try:
                article_body = article_body_element.text_content().strip()
            except AttributeError:
                article_body = ""


            # Append the parsed data to the list
            parsed_data.append({
                "title": title,
                "date": date,
                "duration": duration,
                "teaser": teaser,
                "article_body": article_body
            })

    # Call the function to prioritize the "topNews" elements based on repair start date
    prioritized_top_news = prioritize_top_news(parsed_data)
    # If there are prioritized top news items, select the first item
    if prioritized_top_news:
        top_news =[prioritized_top_news[0]] 
        one_news = prioritized_top_news[0]
        #remove all white spaces (if there is whitespaces we cannot see it in mediawiki id and in the page, but the parsed_content will have white spaces)
        cleaned_top_news = re.sub(r'\s+', ' ', one_news["title"])  
        encoded_title = urllib.parse.quote(cleaned_top_news, safe='')
        # Adapt the encoded_title for compatibility with MediaWiki encoding:
        # - Replace '%20' with underscores ('_')
        # - Replace '%' with periods ('.')
        encoded_title = encoded_title.replace("%20", "_")
        encoded_title = encoded_title.replace("%", ".")  
        see_more_url = f'{HTTP_OR_SSL}{HOSTNAME}/article/Meldungen/#{encoded_title}' #see_more_url for the link to the wiki page
    else:
        top_news = []
        see_more_url = ""
    return top_news, see_more_url

    geoportal_context = GeoportalContext(request)
    top_news, see_more_url = parse_wiki_data()  #added by D. Parajuli
    context_data = geoportal_context.get_context()
    if context_data['dsgvo'] == 'no' and context_data['loggedin'] == True and wiki_keyword not in dsgvo_list:
        return redirect('useroperations:change_profile')

    if wiki_keyword == "viewer":
        template = "geoportal.html"
    elif wiki_keyword != "":
        # display the wiki article in the template
        template = "wiki.html"
        try:
            output = useroperations_helper.get_wiki_body_content(wiki_keyword, lang)
            request.session["current_page"] = wiki_keyword
        except (error.HTTPError, FileNotFoundError) as e:
            template = "404.html"
            output = ""
    else:
        # display the favourite WMCs in the template
        template = "landing_page.html"
        results = useroperations_helper.get_landing_page(lang)

    context = {
               "wiki_keyword": wiki_keyword,
               "content": output,
               "results": results,
               "mobile_wmc_id": MOBILE_WMC_ID,
               #added by D. Parajuli
                "see_more_url": see_more_url,
                "top_news": top_news,
               }
    geoportal_context.add_context(context=context)

    # check if this is an ajax call from info search
    if get_params.get("info_search", "") == 'true':
        category = get_params.get("category", "")
        output = useroperations_helper.get_wiki_body_content(wiki_keyword, lang, category)
        return GeoportalJsonResponse(html=output).get_response()
    else:
        return render(request, template, geoportal_context.get_context())
