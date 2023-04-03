import requests
from bs4 import BeautifulSoup

def get_google_podcasts_link_end(podcast_series_name):
    # format the search query
    query = f"{podcast_series_name} podcast google podcasts"
    query = query.replace(" ", "%20") ##this is the structure of how google podcasts searches look
    url = f"https://podcasts.google.com/search/{query}"
    
    # perform the search and get the HTML response
    response = requests.get(url)
    ##soup = BeautifulSoup(response.text, "html.parser")
    soup = BeautifulSoup(response.content, "html.parser")
    
    # extract the link to the Google Podcasts page, if available
    link = soup.find("a", {"class": "yXo2Qc"})
    ###print('Here is the code that should include the link')
    ###print(link)
    if link:
        return link["href"]
    else:
        #print("******** No Google Podcasts link found. ********")
        return "No Google Podcasts link found."

def get_google_podcasts_link(podcast_series_name):
    #podcast_name = input("Please enter the name for the name of the podcast series you are looking for: \n")
    google_podcasts_link = get_google_podcasts_link_end(podcast_series_name)
    return (f"https://podcasts.google.com{(google_podcasts_link[1:])}")



def main():
    podcast_name = input("Please enter the name for the podcast you are looking for: \n")
    google_podcasts_link = get_google_podcasts_link_end(podcast_name)
    #print(f"Link to {podcast_name} on Google Podcasts: https://podcasts.google.com{(google_podcasts_link[1:])}")


if __name__ == '__main__':
    main()