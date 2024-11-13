from bs4 import BeautifulSoup
import requests
page_to_scrape = requests.get("https://proacne-program.com/check")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
print(soup)
ingredients = soup.findAll("div", attrs={"class":"t005__text t-text t-text_md"})
print(ingredients)