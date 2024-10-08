import os
import pandas as pd
from fuzzywuzzy import process
from rapidfuzz import process


def parse_jobs_to_dataframe(accounts):
    data = []

    for account in accounts:
        account_id = account.get('id', 'Unknown')
        account_name = account.get('name', 'Unknown')
        account_status = account.get('account_status', {}).get('name', 'Unknown')
        addresses = account.get('addresses', {}).get('entities', [])
        contacts = account.get('contacts', {}).get('entities', [])

        if not addresses:
            rowData = {
                "Account ID": account_id,
                "Name": account_name,
                "Status": account_status,
                "Address": 'Unknown',
                "City": 'Unknown',
                "State": 'Unknown',
                "Zip": 'Unknown',
                "Email": 'Unknown',
                "Phone": 'Unknown',
            }
            data.append(rowData)
        else:
            for address in addresses:
                city = address.get('city', 'Unknown')
                state = address.get('subdivision', 'Unknown')[3:]
                zip_code = address.get('zip', 'Unknown')[:5]

                if city.lower() in ['mckinney', 'mc kinney']:
                    city = 'McKinney'

                state = state if state != 'Unknown' else state
                zip_code = zip_code if zip_code != 'Unknown' else zip_code

                if contacts:
                    for contact in contacts:
                        phone = contact.get('phone_numbers', {}).get('entities', [])
                        email = contact.get('email_address', 'Unknown')

                        if isinstance(email, list) and email:
                            email = email[0]
                        elif not email or email == 'Unknown':
                            email = 'Unknown'

                        phone_number = 'Unknown'
                        if phone:
                            phone_number = phone[0].get('number', 'Unknown')

                        formatted_phone = format_phone_number(phone_number)

                        rowData = {
                            "Account ID": account_id,
                            "Name": account_name,
                            "Status": account_status,
                            "Address": address.get('line1', 'Unknown'),
                            "City": city,
                            "State": state,
                            "Zip": zip_code,
                            "Email": email,
                            "Phone": formatted_phone,
                        }
                        data.append(rowData)
                else:
                    rowData = {
                        "Account ID": account_id,
                        "Name": account_name,
                        "Status": account_status,
                        "Address": address.get('line1', 'Unknown'),
                        "City": city,
                        "State": state,
                        "Zip": zip_code,
                        "Email": 'Unknown',
                        "Phone": 'Unknown',
                    }
                    data.append(rowData)

    df = pd.DataFrame(data)

    df_cleaned = df.drop_duplicates(subset=['Account ID'])

    print("Number of records saved:", len(df_cleaned))
    return df_cleaned


def format_phone_number(phone_number):
    digits = ''.join(filter(str.isdigit, phone_number))

    if digits.startswith('1'):
        digits = digits[1:]

    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

    return 'Unknown'

'''
def read_and_clean_arlington() -> pd.DataFrame:
    if not os.path.exists('Arlington Address Details.xlsx'):
        raise FileNotFoundError("Arlington Address Details.xlsx not found.")
    if not os.path.exists('accounts.csv'):
        raise FileNotFoundError("accounts.csv not found.")

    bom_arlington_df = pd.read_excel('Arlington Address Details.xlsx', sheet_name='Arlington_All')
    columns = ['Street_Number', 'Street_Name', 'City', 'FDAName', 'FDHName']
    df_selected = bom_arlington_df[columns]

    df_selected['Street_Name'] = (
        df_selected['Street_Name']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    df_selected['Address'] = df_selected['Street_Number'].astype(str) + ' ' + df_selected['Street_Name']
    df_selected['City'] = (
        df_selected['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    df_selected.drop(columns=['Street_Number', 'Street_Name'], inplace=True)

    print("Cleaned Arlington DataFrame:")
    print(df_selected[['Address', 'City']].head())

    account_df = pd.read_csv('accounts.csv')
    account_df['Address'] = (
        account_df['Address']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )

    account_df['City'] = (
        account_df['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    print("\nCleaned Accounts DataFrame:")
    print(account_df[['Address', 'City']].head())
    unique_addresses = df_selected['Address'].unique()

    matched_addresses = []
    for address in account_df['Address']:
        if address:
            match = process.extractOne(address, unique_addresses, score_cutoff=80)  # Adjust score_cutoff as needed
            if match:
                matched_addresses.append(match[0])
            else:
                matched_addresses.append(None)
        else:
            matched_addresses.append(None)

    account_df['Matched_Address'] = matched_addresses
    merged_df = pd.merge(account_df, df_selected, left_on='Matched_Address', right_on='Address', how='left')

    print("\nMerged DataFrame:")
    print(merged_df.head())

    #return merged_df

    selected_columns = ['Account ID', 'Name', 'Status', 'Address_x', 'City_x', 'State', 'Zip',
                        'Email', 'Phone', 'FDAName', 'FDHName']
    final_df = merged_df[selected_columns]

    final_df = final_df.rename(columns={
        'Address_x': 'Address',
        'City_x': 'City',
        'FDAName': 'FDA',
        'FDHName': 'FDH'
    })

    print("\nFinal DataFrame with selected columns:")
    print(final_df.head())

    return final_df
'''

def read_and_clean_arlington() -> pd.DataFrame:
    if not os.path.exists('Arlington Address Details.xlsx'):
        raise FileNotFoundError("Arlington Address Details.xlsx not found.")
    if not os.path.exists('accounts.csv'):
        raise FileNotFoundError("accounts.csv not found.")

    bom_arlington_df = pd.read_excel('Arlington Address Details.xlsx', sheet_name='Arlington_All')
    columns = ['Street_Number', 'Street_Name', 'City', 'FDAName', 'FDHName']
    df_selected = bom_arlington_df[columns]

    df_selected['Street_Name'] = (
        df_selected['Street_Name']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    df_selected['Address'] = df_selected['Street_Number'].astype(str) + ' ' + df_selected['Street_Name']
    df_selected['City'] = (
        df_selected['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    df_selected.drop(columns=['Street_Number', 'Street_Name'], inplace=True)

    print("Cleaned Arlington DataFrame:")
    print(df_selected[['Address', 'City']].head())

    account_df = pd.read_csv('accounts.csv')
    account_df['Address'] = (
        account_df['Address']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    account_df['City'] = (
        account_df['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    print("\nCleaned Accounts DataFrame:")
    print(account_df[['Address', 'City']].head())

    df_selected['Address_City'] = df_selected['Address'] + ', ' + df_selected['City']
    account_df['Address_City'] = account_df['Address'] + ', ' + account_df['City']

    account_df_arlington = account_df[account_df['City'] == 'Arlington']

    unique_address_city = df_selected['Address_City'].unique()

    matched_addresses = []
    for address_city in account_df_arlington['Address_City']:
        if address_city:
            match = process.extractOne(address_city, unique_address_city, score_cutoff=80)  # Adjust score_cutoff as needed
            if match:
                matched_addresses.append(match[0])
            else:
                matched_addresses.append(None)
        else:
            matched_addresses.append(None)

    account_df_arlington['Matched_Address_City'] = matched_addresses

    merged_df = pd.merge(account_df_arlington, df_selected, left_on='Matched_Address_City', right_on='Address_City', how='left')

    print("\nMerged DataFrame:")
    print(merged_df.head())

    selected_columns = ['Account ID', 'Name', 'Status', 'Address_x', 'City_x', 'State', 'Zip', 'Email', 'Phone', 'FDAName', 'FDHName']
    final_df = merged_df[selected_columns]

    final_df = final_df.rename(columns={
        'Address_x': 'Address',
        'City_x': 'City',
        'FDAName': 'FDA',
        'FDHName': 'FDH'
    })

    print("\nFinal DataFrame with selected columns:")
    print(final_df.head())

    return final_df

'''
def read_and_clean_mckinney() -> pd.DataFrame:
    if not os.path.exists('McKinney Address Details.xlsx'):
        raise FileNotFoundError("McKinney Address Details.xlsx not found.")
    if not os.path.exists('accounts.csv'):
        raise FileNotFoundError("accounts.csv not found.")

    mck_df = pd.read_excel('McKinney Address Details.xlsx', sheet_name='McK_All')
    columns = ['Street_Number', 'Street_Name', 'City', 'FDAName', 'FDHName']
    df_selected = mck_df[columns]

    df_selected['Street_Name'] = (
        df_selected['Street_Name']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    df_selected['Address'] = df_selected['Street_Number'].astype(str) + ' ' + df_selected['Street_Name']
    df_selected['City'] = (
        df_selected['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    df_selected.drop(columns=['Street_Number', 'Street_Name'], inplace=True)

    print("Cleaned McKinney DataFrame:")
    print(df_selected[['Address', 'City']].head())
    account_df = pd.read_csv('accounts.csv')

    account_df['Address'] = (
        account_df['Address']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )

    account_df['City'] = (
        account_df['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    print("\nCleaned Accounts DataFrame:")
    print(account_df[['Address', 'City']].head())

    unique_addresses = df_selected['Address'].unique()
    matched_addresses = []
    for address in account_df['Address']:
        if address:
            match = process.extractOne(address, unique_addresses, score_cutoff=80)  # Adjust score_cutoff as needed
            if match:
                matched_addresses.append(match[0])
            else:
                matched_addresses.append(None)
        else:
            matched_addresses.append(None)

    account_df['Matched_Address'] = matched_addresses
    merged_df = pd.merge(account_df, df_selected, left_on='Matched_Address', right_on='Address', how='left')

    print("\nMerged DataFrame:")
    print(merged_df.head())

    #return merged_df

    selected_columns = ['Account ID', 'Name', 'Status', 'Address_x', 'City_x', 'State', 'Zip',
                        'Email', 'Phone', 'FDAName', 'FDHName']
    final_df = merged_df[selected_columns]

    final_df = final_df.rename(columns={
        'Address_x': 'Address',
        'City_x': 'City',
        'FDAName': 'FDA',
        'FDHName': 'FDH'
    })

    print("\nFinal DataFrame with selected columns:")
    print(final_df.head())

    return final_df
'''

def read_and_clean_mckinney() -> pd.DataFrame:
    if not os.path.exists('McKinney Address Details.xlsx'):
        raise FileNotFoundError("McKinney Address Details.xlsx not found.")
    if not os.path.exists('accounts.csv'):
        raise FileNotFoundError("accounts.csv not found.")

    mck_df = pd.read_excel('McKinney Address Details.xlsx', sheet_name='McK_All')
    columns = ['Street_Number', 'Street_Name', 'City', 'FDAName', 'FDHName']
    df_selected = mck_df[columns]

    df_selected['Street_Name'] = (
        df_selected['Street_Name']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    df_selected['Address'] = df_selected['Street_Number'].astype(str) + ' ' + df_selected['Street_Name']
    df_selected['City'] = (
        df_selected['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    df_selected.drop(columns=['Street_Number', 'Street_Name'], inplace=True)

    print("Cleaned McKinney DataFrame:")
    print(df_selected[['Address', 'City']].head())

    account_df = pd.read_csv('accounts.csv')

    account_df['Address'] = (
        account_df['Address']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    account_df['City'] = (
        account_df['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    print("\nCleaned Accounts DataFrame:")
    print(account_df[['Address', 'City']].head())

    account_df_mckinney = account_df[account_df['City'] == 'Mckinney']

    unique_addresses = df_selected['Address'].unique()

    matched_addresses = []
    for address in account_df_mckinney['Address']:
        if address:
            match = process.extractOne(address, unique_addresses, score_cutoff=80)  # Adjust score_cutoff as needed
            if match:
                matched_addresses.append(match[0])
            else:
                matched_addresses.append(None)
        else:
            matched_addresses.append(None)

    account_df_mckinney['Matched_Address'] = matched_addresses

    merged_df = pd.merge(account_df_mckinney, df_selected, left_on='Matched_Address', right_on='Address', how='left')

    print("\nMerged DataFrame:")
    print(merged_df.head())

    selected_columns = ['Account ID', 'Name', 'Status', 'Address_x', 'City_x', 'State', 'Zip', 'Email', 'Phone', 'FDAName', 'FDHName']
    final_df = merged_df[selected_columns]

    final_df = final_df.rename(columns={
        'Address_x': 'Address',
        'City_x': 'City',
        'FDAName': 'FDA',
        'FDHName': 'FDH'
    })

    print("\nFinal DataFrame with selected columns:")
    print(final_df.head())

    return final_df

'''
def read_and_clean_rockwall() -> pd.DataFrame:
    if not os.path.exists('Rockwall Homes Detail .xlsx'):
        raise FileNotFoundError("Rockwall Homes Detail.xlsx not found.")
    if not os.path.exists('accounts.csv'):
        raise FileNotFoundError("accounts.csv not found.")

    rck_df = pd.read_excel('Rockwall Homes Detail .xlsx', sheet_name='Rockwall_All')
    columns = ['Street_Number', 'Street_Name', 'City', 'FDAName', 'FDHName']
    df_selected = rck_df[columns]

    df_selected['Street_Name'] = (
        df_selected['Street_Name']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    df_selected['Address'] = df_selected['Street_Number'].astype(str) + ' ' + df_selected['Street_Name']

    df_selected['City'] = (
        df_selected['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    df_selected.drop(columns=['Street_Number', 'Street_Name'], inplace=True)

    print("Cleaned Rockwall DataFrame:")
    print(df_selected[['Address', 'City']].head())

    account_df = pd.read_csv('accounts.csv')

    account_df['Address'] = (
        account_df['Address']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )

    account_df['City'] = (
        account_df['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    print("\nCleaned Accounts DataFrame:")
    print(account_df[['Address', 'City']].head())

    unique_addresses = df_selected['Address'].unique()

    matched_addresses = []
    for address in account_df['Address']:
        if address:
            match = process.extractOne(address, unique_addresses, score_cutoff=80)  # Adjust score_cutoff as needed
            if match:
                matched_addresses.append(match[0])
            else:
                matched_addresses.append(None)
        else:
            matched_addresses.append(None)

    account_df['Matched_Address'] = matched_addresses
    merged_df = pd.merge(account_df, df_selected, left_on='Matched_Address', right_on='Address', how='left')

    print("\nMerged DataFrame:")
    print(merged_df.head())

    #return merged_df

    selected_columns = ['Account ID', 'Name', 'Status', 'Address_x', 'City_x', 'State', 'Zip',
                        'Email', 'Phone', 'FDAName', 'FDHName']
    final_df = merged_df[selected_columns]

    final_df = final_df.rename(columns={
        'Address_x': 'Address',
        'City_x': 'City',
        'FDAName': 'FDA',
        'FDHName': 'FDH'
    })

    print("\nFinal DataFrame with selected columns:")
    print(final_df.head())

    return final_df
'''

def read_and_clean_rockwall() -> pd.DataFrame:
    if not os.path.exists('Rockwall Homes Detail.xlsx'):
        raise FileNotFoundError("Rockwall Homes Detail.xlsx not found.")
    if not os.path.exists('accounts.csv'):
        raise FileNotFoundError("accounts.csv not found.")

    rck_df = pd.read_excel('Rockwall Homes Detail.xlsx', sheet_name='Rockwall_All')
    columns = ['Street_Number', 'Street_Name', 'City', 'FDAName', 'FDHName']
    df_selected = rck_df[columns]

    df_selected['Street_Name'] = (
        df_selected['Street_Name']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    df_selected['Address'] = df_selected['Street_Number'].astype(str) + ' ' + df_selected['Street_Name']

    df_selected['City'] = (
        df_selected['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    df_selected.drop(columns=['Street_Number', 'Street_Name'], inplace=True)

    print("Cleaned Rockwall DataFrame:")
    print(df_selected[['Address', 'City']].head())

    account_df = pd.read_csv('accounts.csv')

    account_df['Address'] = (
        account_df['Address']
        .str.lower()
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    account_df['City'] = (
        account_df['City']
        .str.lower()
        .str.strip()
        .str.title()
    )

    print("\nCleaned Accounts DataFrame:")
    print(account_df[['Address', 'City']].head())

    account_df_rockwall = account_df[account_df['City'] == 'Rockwall']

    unique_addresses = df_selected['Address'].unique()

    matched_addresses = []
    for address in account_df_rockwall['Address']:
        if address:
            match = process.extractOne(address, unique_addresses, score_cutoff=80)  # Adjust score_cutoff as needed
            if match:
                matched_addresses.append(match[0])
            else:
                matched_addresses.append(None)
        else:
            matched_addresses.append(None)

    account_df_rockwall['Matched_Address'] = matched_addresses
    merged_df = pd.merge(account_df_rockwall, df_selected, left_on='Matched_Address', right_on='Address', how='left')

    print("\nMerged DataFrame:")
    print(merged_df.head())

    selected_columns = ['Account ID', 'Name', 'Status', 'Address_x', 'City_x', 'State', 'Zip',
                        'Email', 'Phone', 'FDAName', 'FDHName']
    final_df = merged_df[selected_columns]

    final_df = final_df.rename(columns={
        'Address_x': 'Address',
        'City_x': 'City',
        'FDAName': 'FDA',
        'FDHName': 'FDH'
    })

    print("\nFinal DataFrame with selected columns:")
    print(final_df.head())

    return final_df
