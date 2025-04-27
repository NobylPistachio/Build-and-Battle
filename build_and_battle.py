import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm
import time
from collections import defaultdict

BASE_URL = "https://bulbapedia.bulbagarden.net"
SEARCH_URL = "https://bulbapedia.bulbagarden.net/wiki/Template:TCG_Releases"
HEADERS = {"User-Agent": "Mozilla/5.0"}

DECKLIST_KEYWORDS = ["build & battle", "prerelease"]

# def get_article_links(max_pages:int=20):
#     links = []


#     for page in tqdm(range(1, max_pages + 1), desc="Searching Bulbapedia"):
#         url = SEARCH_URL.format(page)
#         r = requests.get(url, headers=HEADERS)
#         soup = BeautifulSoup(r.text, "html.parser")

#         articles = soup.select("small a")
#         for a in articles:
#             title = a.text.lower()
#             if any(kw in title for kw in DECKLIST_KEYWORDS):
#                 links.append((a["href"], a.text.strip()))
#                 print(a["href"], a.text.strip())
#     return links


# def extract_decklists(url):
#     r = requests.get(url, headers=HEADERS)
#     soup = BeautifulSoup(r.text, "html.parser")

def parse_decklist_to_file(html_file, output_file="decklist.txt"):
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    card_tables = soup.find_all("table", {"class": "roundy"})

    cards = defaultdict(int)

    for table in tqdm(card_tables, desc="Scraping Cards"):
        rows = table.find_all("tr")[2:]  # Skip headers
        
        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) < 4:
                continue

            card_link = cells[1].find("a")
            quantity_cell = cells[3]
            if card_link and quantity_cell:
                name = card_link.text.strip()
                quantity_text = quantity_cell.text.strip().replace('×', '')

                if "-" in quantity_text:
                    quantity = int(quantity_text.split('-')[1])  # Use maximum if 1-2×
                else:
                    quantity = int(quantity_text)

                cards[name] += quantity

    # Categorizing cards into Pokémon, Trainer, Energy
    pokemon_keywords = ["Pikachu", "Charizard", "Lucario", "Delphox", "Seel", "Braixen", "Hawlucha", "Carbink", "Dreepy", "Dragapult", "Duskull", "Dusclops", "Dusknoir", "Binacle", "Barbaracle", "Budew", "Fezandipiti", "Bloodmoon Ursaluna"]  # Extend as needed
    energy_keywords = ["Energy"]
    
    pokemon = {}
    trainers = {}
    energies = {}

    for card_name, qty in cards.items():
        if any(word in card_name for word in energy_keywords):
            energies[card_name] = qty
        elif any(word in card_name for word in pokemon_keywords):
            pokemon[card_name] = qty
        else:
            trainers[card_name] = qty

    def write_section(title, section_cards, file):
        file.write(f"{title}: {sum(section_cards.values())}\n")
        for name, qty in sorted(section_cards.items(), key=lambda x: (-x[1], x[0])):
            # No set codes available here, just put name
            file.write(f"{qty} {name}\n")
        file.write("\n")

    # Write to a file
    with open(output_file, "w", encoding="utf-8") as f:
        write_section("Pokémon", pokemon, f)
        write_section("Trainer", trainers, f)
        write_section("Energy", energies, f)

    print(f"Decklist written to {output_file}")



# Get the soup
def get_soup(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def get_pretty_soup_file(page):
    deck_name = page[1]
    url = page[0]
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    with open(f"{deck_name}.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    

# First find number of links on site
def count_links(soup)->int:
    articles = soup.select("small a")
    return len(articles)


# Get each link and append to list
    # Make tqdm loop over that number
def get_links(soup)->list:
    links = []
    articles = soup.select("small a")
    for link in tqdm(range(1, len(articles)+1), desc="Scraping Bulbapedia"):
        link = articles[link-1]
        if any(kw in link.text.lower() for kw in DECKLIST_KEYWORDS):
            links.append((link["href"], link.text.strip()))
    return links

def create_full_url(url):
    return BASE_URL + url

def scrape_decklist_1(page):
    pass

def scrape_decklist_2(page):
    pass

def scrape_assistant(pageType:int):
    match pageType:
        case 1:
            print("Found 1 section")
        case 2:
            print("Found 2 sections")
        case 0:
            print("No Sections Found, please check page")
        case _:
            print("Invalid page type")
    

def scrape_decklist(page):
    # print(f"🧩 Scraping: {page[1]}")
    url = page[0]
    # Get the soup
    soup = get_soup(url)
    # Scrape each table with class="multicol"
    sections = soup.find_all("table", class_="multicol")
    # Find how many sections are on page
    # Print number of sections
    # scrape_assistant(len(sections))
    # Check for "roundy"
    # Scrape each table with class="roundy"
    # for table in sections:
    pass

# Make tqdm loop over list
# Scrape each link for decklist

    
def main():
    soup = get_soup(SEARCH_URL)
    links = get_links(soup)
    pages = [(create_full_url(link[0]), link[1]) for link in links]
    
    with tqdm(total=len(pages),desc="Getting Webpages From Bulbapedia") as pbar:
        for page in pages:
            tqdm.write(f"Started: {page[1]}")
            scrape_decklist(page)
            pbar.update(1)

    # for page in tqdm(range(1, len(pages)+1), desc="Getting Webpages From Bulbapedia"):
    #     page = pages[page-1]
    #     scrape_decklist(page)
    print(pages[0])
        
def test():
    soup = get_soup(SEARCH_URL)
    links = get_links(soup)
    pages = [(create_full_url(link[0]), link[1]) for link in links]
    get_pretty_soup_file(pages[0])
    parse_decklist_to_file(f"{pages[0][1]}.html", f"{pages[0][1]}.txt")
    
if __name__ == "__main__":
    main()








