# Import necessary modules
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from .models import WikiData
import requests


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
        

        # Initialize a flag to determine if the current section is a topNews section
        in_top_news = False

        # Find all <h2> elements (titles)
        h2_elements = soup.find_all("h2")

        # Loop through each <h2> element (title)
        for h2 in h2_elements:
            # Extract the title
            title = h2.text.strip()
            if "[Bearbeiten]" in title:
                # Remove "[Bearbeiten]" and trim spaces
                title = title.replace("[Bearbeiten]", "").strip()

            


            # Only parse content if we're not in a topNews section
            if not in_top_news:
                # Find the next <p> element containing the date
                date_element = h2.find_next('p').find('strong')

                if date_element:
                    # Extract the date
                    date = date_element.text.strip()

                    # Find all <p> elements containing the description until the next <h2> title
                    description = ""
                    next_elements = date_element.find_all_next()

                    for next_element in next_elements:
                        # Check if the element is an <h2> tag (next title)
                        if next_element.name == 'h2':
                            break  # Stop when the next title is encountered

                        # Check if the element is an <hr> tag
                        if next_element.name == 'hr':
                            # Add the description to the entry
                            entry = {
                                "title": title,
                                "date": date,
                                "description": description.strip()  # Remove leading/trailing whitespace
                            }

                            # Append the JSON object to the list
                            parsed_data.append(entry)

                            # Reset the description for the next section
                            description = ""

                        # Check if the element is a <p> tag
                        if next_element.name == 'p':
                            # Append the text of the <p> tag to the description
                            description += next_element.text.strip() + "\n"

                            # Check for links and make them clickable
                            links = next_element.find_all('a')
                            if links:
                                for link in links:
                                    link_text = link.text.strip()
                                    link_url = link.get('href')
                                    clickable_link = f'<a href="{link_url}">{link_text}</a>'
                                    description += clickable_link + "\n"

                        # Move to the next element
                        next_element = next_element.find_next()

                    # Add the last entry (if any)
                    if description:
                        entry = {
                            "title": title,
                            "date": date,
                            "description": description.strip()  # Remove leading/trailing whitespace
                        }

                        parsed_data.append(entry)

    # Return the parsed data to the HTML template
    return render(request, 'mediawiki/landing_page.html', {'parsed_data': parsed_data})
