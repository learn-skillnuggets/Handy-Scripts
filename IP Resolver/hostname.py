import socket
import openpyxl

def resolve_hostnames(file_name, batch_size=20):
    # Load the Excel file
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active

    # Get all rows with hostnames and prepare for batching
    rows = list(sheet.iter_rows(min_row=2, max_col=2, min_col=1))
    total_rows = len(rows)

    for start in range(0, total_rows, batch_size):
        end = min(start + batch_size, total_rows)
        print(f"Processing rows {start + 1} to {end}...")

        for row in rows[start:end]:
            hostname_cell = row[0]  # Column A (hostname)
            ip_cell = row[1]        # Column B (IP address)

            hostname = hostname_cell.value
            if hostname:
                try:
                    # Resolve the hostname to an IP address
                    ip_address = socket.gethostbyname(hostname)
                    ip_cell.value = ip_address
                except socket.gaierror:
                    # Handle cases where the hostname cannot be resolved
                    ip_cell.value = "Resolution failed"

        # Save progress after each batch
        workbook.save(file_name)
        print(f"Batch {start + 1} to {end} saved.")

# File name of your Excel file (located in the same directory as the script)
file_name = "hostnames.xlsx"
resolve_hostnames(file_name)
print(f"IP addresses have been resolved and saved in {file_name}")
