import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus # automatically added plus sign when spaced (initially %20)
from . import models

BASE_CRAIGSLIST_URL = 'https://newyork.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search) # add objects onto admin site
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # Getting the webpage, creating a Response object
    response = requests.get(final_url)
    # Extracting the source code of the page
    data = response.text
    # Passing the source code to Beautiful Soup to create a BeautifulSoup object for it
    soup = BeautifulSoup(data, features='html.parser')
    # Extracting all the <a> tags whose class name is 'result-title' into a list
    #post_titles = soup.find_all('a', {'class': 'result-title'})

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url   = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        # insert an image for the post
        # Don't care about all of the images just one image
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
            print(post_image_url)

        final_postings.append((post_title, post_url, post_price, post_image_url))

    frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'myapp/new_search.html', frontend)