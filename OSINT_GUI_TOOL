import tkinter as tk
from tkinter import scrolledtext, Checkbutton, BooleanVar, filedialog, ttk
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
        formatted_query = quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={formatted_query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.post(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for link in soup.find_all("a", class_="result__url"):
            href = link.get("href")
            if href:
                results.append(href)

        return results[:num_results]
    except Exception as e:
        return [f"An error occurred: {e}"]

def google_search(query, num_results=10):
    """
    Perform a Google search and return the results.

    :param query: The search query.
    :param num_results: Number of results to retrieve.
    :return: List of URLs.
    """
    try:
        formatted_query = quote_plus(query)
        url = f"https://www.google.com/search?q={formatted_query}&num={num_results}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and "url?q=" in href and not "webcache.googleusercontent.com" in href:
                url = href.split("url?q=")[1].split("&")[0]
                results.append(url)

        return results[:num_results]
    except Exception as e:
        return [f"An error occurred: {e}"]

def bing_search(query, num_results=10):
    """
    Perform a Bing search and return the results.

    :param query: The search query.
    :param num_results: Number of results to retrieve.
    :return: List of URLs.
    """
    try:
        formatted_query = quote_plus(query)
        url = f"https://www.bing.com/search?q={formatted_query}&count={num_results}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.startswith("http"):
                results.append(href)

        return results[:num_results]
    except Exception as e:
        return [f"An error occurred: {e}"]

def perform_search():
    """
    Perform the search and display results in the GUI.
    """
    # Get user input
    name = entry_name.get()
    additional_keywords = entry_keywords.get()
    search_engine = search_engine_var.get()

    # Construct the query
    if additional_keywords:
        query = f'"{name}" {additional_keywords}'
    else:
        query = f'"{name}"'

    # Clear previous results
    result_text.delete(1.0, tk.END)

    # Perform the search based on the selected search engine
    if search_engine == "DuckDuckGo":
        results = duckduckgo_search(query)
    elif search_engine == "Google":
        results = google_search(query)
    elif search_engine == "Bing":
        results = bing_search(query)
    else:
        results = ["Invalid search engine selected."]

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
        result_text.insert(tk.END, f"Search Engine: {search_engine}\n")
        result_text.insert(tk.END, f"Query: {query}\n")
        result_text.insert(tk.END, f"Number of Results: {len(results)}\n")

def save_results():
    """
    Save the search results to a text file.
    """
    results = result_text.get(1.0, tk.END)
    if not results.strip():
        result_text.insert(tk.END, "No results to save.\n")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(results)
        result_text.insert(tk.END, f"Results saved to {file_path}\n")

# Create the main window
root = tk.Tk()
root.title(" GeoConcept's OSINT Recon Tool")

# Set window size
root.geometry("750x500")

# Create and place widgets
label_name = tk.Label(root, text="Name of the person of interest:")
label_name.pack(pady=5)

entry_name = tk.Entry(root, width=50)
entry_name.pack(pady=5)

label_keywords = tk.Label(root, text="Additional keywords (optional):")
label_keywords.pack(pady=5)

entry_keywords = tk.Entry(root, width=50)
entry_keywords.pack(pady=5)

# Search engine dropdown
search_engine_var = tk.StringVar(value="DuckDuckGo")
label_engine = tk.Label(root, text="Select Search Engine:")
label_engine.pack(pady=5)

search_engine_menu = ttk.Combobox(root, textvariable=search_engine_var, values=["DuckDuckGo", "Google", "Bing"])
search_engine_menu.pack(pady=5)

# Debug checkbox
debug_var = BooleanVar()
debug_checkbox = Checkbutton(root, text="Enable Debugging", variable=debug_var)
debug_checkbox.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Search", command=perform_search)
search_button.pack(pady=10)

# Save button
save_button = tk.Button(root, text="Save Results", command=save_results)
save_button.pack(pady=10)

# Results text box
result_text = scrolledtext.ScrolledText(root, width=85, height=20, wrap=tk.WORD)
result_text.pack(pady=10)

# Run the application
root.mainloop()
