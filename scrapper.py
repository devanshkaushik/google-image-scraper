import time
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console

# Setting up rich console
console = Console()

def setupDriver():
  options = webdriver.ChromeOptions()
  options.add_argument("--log-level=3")
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  return driver

def initiate(searchUrl, imageAmt = 50):
  urls = []
  driver = setupDriver()

  driver.get(searchUrl)

  console.log(f"[cyan]Press enter to start scraping...", end="")
  _ = input()

  # Scrolling to the top
  driver.execute_script("window.scrollTo(0, 0);")

  pageHtml = driver.page_source
  pageSoup = bs4.BeautifulSoup(pageHtml, "html.parser")
  containers = pageSoup.findAll("a", {"class": "wXeWr islib nfEiy"})

  containerLen = len(containers)

  if containerLen < imageAmt:
    imageAmt = containerLen
    console.log(f"[red]Not enough image found.[/red] Setting the image amount to ", imageAmt)

  # Initializing the count variabels
  scrapedImageAmt = 0
  count = 1

  with console.status("[bold green]Scraping images...") as status:
    while scrapedImageAmt < imageAmt:
      # * xPath with id multiple of 25 doesn't work. Related Searches show up at that path.
      # * xPath with id=217 doesn't work. Related Searches show up at that path.
      if count % 25 == 0 or count == 217:
        count += 1
        continue

      xPath = f'//*[@id="islrg"]/div[1]/div[{count}]'

      # Getting the Url of the thumbnail image
      thumbImageXPath = f'//*[@id="islrg"]/div[1]/div[{count}]/a[1]/div[1]/img'
      thumbImageElement = driver.find_element(by=By.XPATH, value=thumbImageXPath)
      thumbImageUrl = thumbImageElement.get_attribute("src")

      # Clicking the image container
      driver.find_element(by=By.XPATH, value=xPath).click()

      timeStarted = time.time()

      # Waiting for the image to load
      while True:
        imageElement = driver.find_element(by=By.XPATH, value=f'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')
        imageUrl = imageElement.get_attribute("src")

        if imageUrl != thumbImageUrl:
          urls.append(imageUrl)
          scrapedImageAmt += 1
          console.log(f"[green]Scraped image[/green] {scrapedImageAmt}/{imageAmt}")
          break

        else:
          currentTime = time.time()
          if currentTime - timeStarted > 10:
            console.log(f"[red]Timeout![/red] Will continue scraping other images")
            break

      count += 1

  console.log(f"[bold][red]Done scraping image urls")
  return urls

if __name__ == "__main__":
  initiate("https://www.google.com/search?q=apple&source=lnms&tbm=isch", 10)
