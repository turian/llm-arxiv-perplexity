import asyncio
import sys
import os
import os.path 

import datetime
import aiohttp
import re
import chardet
import html2text
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from tqdm import tqdm
import hashlib


async def get_html(url):
    # Launch an instance of Playwright
    async with async_playwright() as p:
        # Start the browser
        browser = await p.chromium.launch()
        # Open a new page
        page = await browser.new_page()
        # Navigate to the URL
        await page.goto(url)
        # Wait for 5 seconds to ensure the page has fully loaded
        await asyncio.sleep(5)
        # Get the page content
        content = await page.content()
        # Close the browser
        await browser.close()
        return content


async def fetch_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


def utf8text(byts):
    result = chardet.detect(byts)
    encoding = result["encoding"]
    text = None
    if not encoding:
        encoding = "utf-8"
    try:
        text = byts.decode(encoding, "ignore")
    except Exception as e:
        print(e, sys.stderr)
        try:
            text = byts.decode(encoding.lower(), "ignore")
        except Exception as e:
            print(e, sys.stderr)
            try:
                text = byts.decode(encoding.lower().replace("-", "_"), "ignore")
            except Exception as e:
                print(e, sys.stderr)
                text = byts.decode("utf-8", "ignore")
    assert text is not None
    return text
    # text = byts.decode(encoding)
    # open(temp.name, "wt").write(text)


def filtered_lines(text):
    """
    Filter out lines that start with 'Generated on'
    which is almost always the last line(s) of the text
    """
    # Split the text into lines
    lines = text.split('\n')
    filtered_lines = []
    for line in lines:
        if not line.startswith('Generated on'):
            filtered_lines.append(line)
        else:
            break
    return "\n".join(filtered_lines)

def hash4slug(slug):
    return hashlib.sha1(slug.encode()).hexdigest()[:4]


async def main():
    now = datetime.datetime.now()
    nowstr = now.strftime("%Y-%m-%d-%H:%M:%S")
    print(f"Starting at {nowstr}")

    workdir = f"data/{nowstr}/papers/"
    if not os.path.exists(workdir):
        os.makedirs(workdir)

    url = "https://deeplearn.org/"
    html_content = await get_html(url)
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")
    # Find all div elements with class 'panel'
    divs = soup.find_all("div", class_="panel")
    # Filter divs to keep only those with a child h3 with text 'Hot Papers'
    filtered_divs = [div for div in divs if div.find("h3", text="Hot Papers")]

    hot_urls = set()

    # Print each filtered div prettified
    for div in filtered_divs:
        buttons = div.find_all("button", onclick=True)
        for button in buttons:
            # Extract the URL from the onclick attribute
            onclick_content = button["onclick"]
            url = onclick_content.split("'")[
                1
            ]  # This splits the string and extracts the URL
            if not url.startswith("http://arxiv.org/pdf/"):
                continue
            hot_urls.add(url)

    for url in tqdm(list(hot_urls)):
        url = url.replace("arxiv.org/pdf", "arxiv.org/html")
        slug = url.split("/")[-1]
        hash4 = hash4slug(slug)
        print(f"Processing {hash4} {slug}")
        htmlbytes = await fetch_page(url)
        html = utf8text(htmlbytes)
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text = text_maker.handle(html)
        filtered_text = filtered_lines(text)

        with open(f"{workdir}/{hash4}-{slug}.txt", "wt") as f:
            f.write(filtered_text)

# Run the main function
asyncio.run(main())
