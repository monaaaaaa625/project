import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

# Constants for URL and headers
URL = "https://www.75mall.com/it-and-elektronike/all-in-one/laptop-standard/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    )
}


def fetch_page_content(url):
    """Fetches the HTML content of the page."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve the page. Status Code:", response.status_code)
        return None


def parse_laptop_data(laptop_div):
    """Extracts title, price, and discount price from a single product listing."""
    title_element = laptop_div.find('a', class_='product-title')
    price_element = laptop_div.find('span', class_='ty-list-price')
    discount_price_element = laptop_div.find('span', class_='ty-price-update')

    # Extract text and clean
    title = title_element.text.strip() if title_element else 'N/A'
    price = clean_price(price_element.text) if price_element else None
    discount_price = clean_price(discount_price_element.text) if discount_price_element else None

    return {'Title': title, 'Price': price, 'Discount Price': discount_price}


def clean_price(price_text):
    """Converts price text to a float after removing symbols."""
    try:
        return float(price_text.replace('€', '').replace(',', '')) / 100
    except (ValueError, AttributeError):
        return None  # Use None for missing or invalid prices


def scrape_laptops():
    """Main function to scrape laptops and display a DataFrame and plot."""
    page_content = fetch_page_content(URL)
    if not page_content:
        return

    # Parse HTML content
    soup = BeautifulSoup(page_content, 'html.parser')
    product_divs = soup.find_all('div', class_='ty-column4')  # Adjust class if needed

    # Extract laptop data
    laptops = [parse_laptop_data(div) for div in product_divs[:10]]  # Limit to first 10 products

    # Create DataFrame
    df = pd.DataFrame(laptops)
    print(df)  # Display the DataFrame

    # Plot the data
    plot_data(df)


def plot_data(df):
    """Creates a bar plot for the laptop prices and discount prices."""
    # Melt the DataFrame to a long format for plotting with Plotly
    df_melted = df.melt(id_vars="Title", value_vars=["Price", "Discount Price"],
                        var_name="Type", value_name="Price (EUR)")

    # Plot the data
    fig = px.bar(df_melted, x="Title", y="Price (EUR)", color="Type",
                 title="Laptop Prices vs. Discount Prices",
                 labels={'Price (EUR)': 'Price (EUR)', 'Type': 'Price Type'})
    fig.update_layout(xaxis_title="Laptop Model", yaxis_title="Price (EUR)", xaxis_tickangle=-45)
    fig.show()


# Call the function to scrape data
scrape_laptops()
