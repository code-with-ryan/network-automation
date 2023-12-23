# This script connects to a network device using the Napalm library,
# retrieves information about the device, and adds the device details to an inventory.
# The inventory is then exported to an Excel file using the pandas library.

# Before running the script, make sure to set the environment variables USERNAME and PASSWORD
# with the appropriate credentials for accessing the network device.

# Required libraries
from napalm import get_network_driver
import pandas as pd
import os
import json
import datetime

# Get credentials from environment variables
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

# Get today's date
today = datetime.date.today()

# Excel file details
EXCEL_NAME = "Network Device Inventory - {today}"
EXCEL_PATH = "./"

# IP address of the network device (replace with the actual IP address)
ip_addresses = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]

# List to store device information in the inventory
inventory = []

for ip_address in ip_addresses:
    try:
        # Connect to the network device
        print(f"Connecting to {ip_address}")
        cisco_driver = get_network_driver("ios")
        connection = cisco_driver(ip_address, USERNAME, PASSWORD)
        connection.open()
    
        # Gather device information
        print(f"Gathering facts from {ip_address}")
        facts = connection.get_facts()
    
        # Create a dictionary with device details
        device = {
            "hostname": facts["hostname"],
            "ip address": ip_address,
            "vendor": facts["vendor"],
            "model": facts["model"],
            "operating system": facts["os_version"],
            "serial number": facts["serial_number"],
            "date": today  # Add today's date to the device details
        }
    
        # Add device to the inventory
        print(f"Adding {ip_address} to inventory")
        print(device)
        inventory.append(device)
    
    except Exception as e:
        print(f"There has been an error connecting to {ip_address}: {e}")

# Convert the inventory to a pandas DataFrame
df = pd.DataFrame(inventory)

# Export the inventory to an Excel file
df.to_excel(f"{EXCEL_PATH}{EXCEL_NAME}_{today}.xlsx", index=False)  # Include today's date in the Excel file name

