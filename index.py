import scrapper
import requests
import os
import uuid
from rich.console import Console

# Setting up rich console
console = Console()

queries = {
  "power_supply": "https://www.google.co.in/search?q=dc+power+supply&tbm=isch&tbs=rimg:CUVDDZ3UEHUUYYi1gnPSGUQZ8AEAsgIOCgIIABAAKAE6BAgBEAE",
  "soldering_iron": "https://www.google.com/search?q=soldering+iron&tbm=isch&tbs=rimg:CSKOMKqp0C23YXegjTwLdKzy8AEAsgIOCgIIABAAKAE6BAgBEAE",
  "3d_printer": "https://www.google.co.in/search?q=3d%20printer&tbm=isch&tbs=rimg:CV1jCh1MCCcLYXJNELxa1M70sgIOCgIIABAAKAE6BAgBEAE"
}

def downloadImage(url, folderName, imageId, imageFormat):
  try:
    # Try to send request for the provided image url
    response = requests.get(url, timeout=10)
    if response.status_code == 200: # * Status Code 200: OK
      imageName = f"{str(imageId)}.{imageFormat}"
      fileName = os.path.join(folderName, imageName)

      # Creating the directory if not already created
      os.makedirs(os.path.dirname(fileName), exist_ok=True)

      with open(fileName, "wb") as file:
        file.write(response.content)
  except:
    console.log(f"[red]Failed to download image: {url}[/red] Will continue downloading other images")

if __name__ == "__main__":

  for item, query in queries.items():
    console.log(f"[bold][yellow]Query item: {item}")

    folderName = os.path.join("images", item)

    imageUrls = scrapper.initiate(query, 10)

    with console.status("[bold green]Downloading scrapped images...") as status:
      for i, imageUrl in enumerate(imageUrls):
        console.log(f"[green]Downloading image {i+1}/{len(imageUrls)} [/green] {imageUrl}")
        downloadImage(imageUrl, folderName, uuid.uuid1(), "jpg")

  console.log(f"[bold][red]Done!")
