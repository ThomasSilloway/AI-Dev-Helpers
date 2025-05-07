# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests>=2.20",
# ]
# ///

# This block above is a special comment that uv (and other tools
# supporting PEP 723) can read to understand the script's dependencies.
#
# How to use with uv:
# 1. Save this file (e.g., as hello_uv.py).
# 2. Make sure you have uv installed (https://github.com/astral-sh/uv).
# 3. Run the script directly using uv:
#    uv run hello_uv.py
#
#    uv will automatically create a virtual environment (if needed),
#    install the specified dependencies (like 'requests'), and then
#    execute the script within that environment.
#
# To add a new dependency:
#   You can manually edit the `dependencies` list above, or
#   use the command: `uv add --script hello_uv.py new_package_name`
#   uv will then update this script file with the new dependency.

import requests
import sys

def fetch_example_data():
    """
    Fetches a small piece of data from a public API using the requests library.
    """
    try:
        response = requests.get("https://httpbin.org/get")
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        data = response.json()
        print("Successfully fetched data:")
        print(f"  Origin IP: {data.get('origin')}")
        print(f"  User-Agent: {data.get('headers', {}).get('User-Agent')}")
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch data: {e}")
        sys.exit(1)

def main():
    """
    Main function to print a hello message and demonstrate dependency usage.
    """
    print("Hello from a Python script managed by uv!")
    print("This script uses the 'requests' library specified in its header.")
    print(f"Running with Python version: {sys.version.split()[0]}")
    print("-" * 30)
    fetch_example_data()
    print("-" * 30)
    print("Script execution finished.")

if __name__ == "__main__":
    main()
