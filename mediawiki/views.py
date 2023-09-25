# Import necessary modules
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup
import datetime
from django.shortcuts import render
from urllib.parse import quote
import urllib


import requests

def prioritize_top_news(parsed_data):
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
    sorted_data = sorted(parsed_data, key=custom_sort)

    # Filter out "topNews" items with repair dates that have already passed
    sorted_data = [item for item in sorted_data if custom_sort(item) >= 0]

    return sorted_data

def parse_wiki_data(request):
    # Define the URL of your Wikimedia API endpoint
    api_url = "https://test.geoportal.hessen.de/mediawiki/api.php"

    # Define parameters for the API request to parse the "Meldungen" page
    params = {
        "action": "parse",
        "format": "json",
        "page": "Meldungen",  # Replace with the title of your desired page
        "formatversion": 2
    }

    # Make the API request
    response = requests.get(api_url, params=params)

    # Initialize a list to store the parsed data
    parsed_data = []

    # Check if the API request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        parsed_content = data["parse"]["text"]

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(parsed_content, "html.parser")
        
        # Find all div elements with class="topNews" 
        top_news_elements = soup.find_all("div", class_="topNews")
        
        # Loop through each topNews element
        for top_news in top_news_elements:
            # Extract the title
            title = top_news.find("h2").text.strip()

            # Extract the date
            date = top_news.find("p").find("strong").text.strip()

            # Extract if the duration time if the span class is "hiddenDuration"
            duration = top_news.find("span", class_="hiddenDuration")
            if duration:
                duration = duration.text.strip()
            else:
                duration = ""

            # Extract the teaser if the p class is "teaser"
            teaser = top_news.find("p", class_="teaser")
            if teaser:
                teaser = teaser.text.strip()
            else:
                teaser = ""

            # Extract the articleBody if the p class is "articleBody"
            article_body = top_news.find("p", class_="articleBody")
            if article_body:
                article_body = article_body.text.strip()
            else:
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
    if prioritized_top_news:
        top_news =[prioritized_top_news[0]] 
        one_news = prioritized_top_news[0]
        title_with_underscore= one_news["title"].replace(" ", "_")
       
        #change the date inte
        see_more_url = f'https://test.geoportal.hessen.de/article/Meldungen/#{title_with_underscore}'  
        
        
    else:
        top_news = []
        see_more_url = ""

   
        

    # Render the prioritized_top_news in the landing page
    return render(request, 'mediawiki/landing_page.html', {'top_news': top_news, 'see_more_url': see_more_url})
