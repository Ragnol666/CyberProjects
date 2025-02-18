import tkinter as tk
from tkinter import scrolledtext, Checkbutton, BooleanVar
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def duckduckgo_search(query, num_results=10):
    """
    Perform a DuckDuckGo search and return the results.

    :param query: The search query.
    :param num_results: Number of results to retrieve.
    :return: List of URLs.
    """
    try:
        # Format the query for DuckDuckGo search
        formatted_query = quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={formatted_query}"

        # Set headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Send the request
        response = requests.post(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract search result links
        results = []
        for link in soup.find_all("a", class_="result__url"):
            href = link.get("href")
            if href:
                results.append(href)

        return results[:num_results]  # Return only the requested number of results
    except Exception as e:
        return [f"An error occurred: {e}"]

def perform_search():
    """
    Perform the search and display results in the GUI.
    """
    # Get user input
    name = entry_name.get()
    additional_keywords = entry_keywords.get()

    # Construct the query
    if additional_keywords:
        query = f'"{name}" {additional_keywords}'
    else:
        query = f'"{name}"'

    # Clear previous results
    result_text.delete(1.0, tk.END)

    # Perform the search
    result_text.insert(tk.END, f"Searching for: {query}\n\n")
    results = duckduckgo_search(query)

    # Display results
    if results and not results[0].startswith("An error occurred"):
        result_text.insert(tk.END, f"Found {len(results)} results:\n")
        for i, url in enumerate(results, 1):
            result_text.insert(tk.END, f"{i}. {url}\n")
    else:
        result_text.insert(tk.END, "No results found.\n")

    # Display debug information if enabled
    if debug_var.get():
        result_text.insert(tk.END, "\nDebug Information:\n")
        result_text.insert(tk.END, f"Query: {query}\n")
        result_text.insert(tk.END, f"Search URL: https://html.duckduckgo.com/html/?q={quote_plus(query)}\n")
        result_text.insert(tk.END, f"Number of Results: {len(results)}\n")

# Create the main window
root = tk.Tk()
root.title(" GeoConcept's OSINT Recon Tool")

# Set window size
root.geometry("700x450")

# Create and place widgets
label_name = tk.Label(root, text="Name of the person of interest:")
label_name.pack(pady=5)

entry_name = tk.Entry(root, width=50)
entry_name.pack(pady=5)

label_keywords = tk.Label(root, text="Additional keywords (optional):")
label_keywords.pack(pady=5)

entry_keywords = tk.Entry(root, width=50)
entry_keywords.pack(pady=5)

# Debug checkbox
debug_var = BooleanVar()
debug_checkbox = Checkbutton(root, text="Enable Debugging", variable=debug_var)
debug_checkbox.pack(pady=5)

search_button = tk.Button(root, text="Search", command=perform_search)
search_button.pack(pady=10)

result_text = scrolledtext.ScrolledText(root, width=85, height=20, wrap=tk.WORD)
result_text.pack(pady=10)

# Run the application
root.mainloop()
