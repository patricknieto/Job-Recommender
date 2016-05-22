from bs4 import BeautifulSoup  # For HTML parsing
import re  # Regular expressions
from time import sleep  # To prevent overwhelming the server between connections
import requests
import pickle


def job_info(city=None, state=None):
    """
    This function will take a desired city/state and look for all new job postings
    on Indeed.com. It will crawl all of the job postings and return all of the words used
    in the posting.

    Inputs: The location's city and state. These are optional. If no city/state is input,
    the function will assume a national search (this can take a while!!!).
    Input the city/state as strings, such as skills_info('Chicago', 'IL').
    Use a two letter abbreviation for the state.

    Output: a list of lists which contain words used in the posting as strings

    """

    final_job = 'data+scientist'  # searching for data scientist exact fit("data scientist" on Indeed search)
    base_url = 'http://www.indeed.com'

    # Make sure the city specified works properly if it has more than one word (such as San Francisco)
    if city is not None:
        final_city = city.split()
        final_city = '+'.join(word for word in final_city)
        final_site_list = ['http://www.indeed.com/jobs?q=%22', final_job, '%22&l=', final_city,
                           '%2C+', state]  # Join all of our strings together so that indeed will search correctly
    else:
        final_site_list = ['http://www.indeed.com/jobs?q="', final_job, '"']

    final_site = ''.join(final_site_list)  # Merge the html address together into one string

    try:
        soup = get_soup(final_site)  # Open up the front page of our search first
    except:
        print('That city/state combination did not have any jobs. Exiting . . .')  # In case the city is invalid
        return

    # Now find out how many jobs there were
    total_num_jobs = search_count(soup)

    city_title = city
    if city is None:
        city_title = 'Nationwide'

    num_pages = int(total_num_jobs/10)
    # This will be how we know the number of times we need to iterate over each new search result page

    print('There were', total_num_jobs, 'jobs found in ', city_title)  # Display how many jobs were found

    job_descriptions = []

    for i in range(1, num_pages+1):  # Loop through all of our search result pages
        print('Getting page', i)
        start_num = str(i*10)  # Assign the multiplier of 10 to view the pages we want
        current_page = ''.join([final_site, '&start=', start_num])
        # Now that we can view the correct 10 job returns, start collecting the text samples from each

        print(current_page)
        page_obj = get_soup(current_page)  # Get the page

        # Locate all of the job links
        job_link_area = page_obj.find(id='resultsCol')  # The center column on the page where the job postings exist

        job_urls = [base_url + link.get('href') for link in job_link_area.find_all('a')]  # Get the URLS for the jobs

        job_func = filter(lambda x: 'clk' in x and 'prime' not in x and 'pagead', job_urls)  # Get just job related URLS

        for j in range(0, len(list(job_func))):
            final_description = text_cleaner(job_urls[j])
            if final_description:  # So that we only append when the website was accessed correctly
                job_descriptions.append(final_description)
            sleep(1)  # So that we don't be jerks. A very fast internet connection can hit the server a lot!

        print('We have %s job descriptions' % len(job_descriptions))

    return job_descriptions


def text_cleaner(website):
    """
    This function just cleans up html from a web page
    Inputs: a URL to investigate
    Outputs: Cleaned text only
    """

    try:
        soup_obj = get_soup(website) # Connect to the job posting
    except:
        return   # Need this in case the website isn't there anymore or some other weird connection problem

    for script in soup_obj(["script", "style"]):
        script.extract()  # Remove these two elements from the BS4 object

    text = soup_obj.get_text() # Get the text from this

    #  COULD BE AN ISSUE HERE!!!!-------BEAUTIFUL SOUP IS COMBINE WORDS AT THE END OF THE LINE WITH THE NEW LINE
    lines = [line.strip() for line in text.splitlines()]  # break into lines

    chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]  # break multi-headlines into a line each

    text = ' '.join(chunk for chunk in chunks if chunk)  # Get rid of all blank lines and ends of line

    text = text.encode('ascii', 'ignore')

    try:
        text = text.decode('unicode_escape').lower().replace('were', 'we\'re')
        #  Need this as some websites aren't formatted in a way that this works, can occasionally throw an exception
    except:
        return

    text = re.sub("[^a-zA-Z0-9+_]", " ", text).replace('were', 'we\'re').split()

    # could possibly make a set here depending on if we want to filter out duplicates

    return text


def get_soup(url):
    """
    This function takes a url string, gathers raw html and returns an html object
    Input: URL string
    Output: soup object

    """

    try:
        r = requests.get(url)
        page = r.text
        soup = BeautifulSoup(page, 'lxml')

        if len(soup) == 0:  # In case the default parser lxml doesn't work, try another one
            soup = BeautifulSoup(page, 'html5lib')

    except requests.ConnectionError:
        print("failed to connect")

    return soup


def search_count(soup):

    num_jobs_area = soup.find(id='searchCount').get_text()  # Now extract the total number of jobs found

    print(num_jobs_area)
    job_numbers = re.findall(r'\d+', num_jobs_area)  # Extract the total jobs found from the search result

    if len(job_numbers) > 3:  # Have a total number of jobs greater than 1000
        total_num_jobs = (int(job_numbers[2])*1000) + int(job_numbers[3])
    else:
        total_num_jobs = int(job_numbers[2])

    return total_num_jobs


jobs = job_info(city='San Francisco', state='CA')

print('pickling...')
with open('jobs_descriptions_SF.pk', 'wb') as handle:
    pickle.dump(jobs, handle)

print('Done with collecting the job postings!')
print('There were', len(jobs), 'jobs successfully found.')


