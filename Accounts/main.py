from Accounts.processing import parse_jobs_to_dataframe, read_and_clean_arlington, read_and_clean_mckinney, \
    read_and_clean_rockwall
from Connection import client
from Query.accounts import fetch_all_jobs


if __name__ == "__main__":
    accounts = fetch_all_jobs(client)
    accounts = parse_jobs_to_dataframe(accounts)
    accounts.to_csv('accounts.csv', index=False)

    cleaned_df_arlington = read_and_clean_arlington()
    cleaned_df_arlington.to_excel('cleaned_df_arlington.xlsx', index=False)
    cleaned_df_mckinney = read_and_clean_mckinney()
    cleaned_df_mckinney.to_excel('cleaned_df_mckinney.xlsx', index=False)
    cleaned_df_rockwall = read_and_clean_rockwall()
    cleaned_df_rockwall.to_excel('cleaned_df_rockwall.xlsx', index=False)

    import pandas as pd

    arlington_df = pd.read_excel('cleaned_df_arlington.xlsx')
    mckinney_df = pd.read_excel('cleaned_df_mckinney.xlsx')
    rockwall_df = pd.read_excel('cleaned_df_rockwall.xlsx')
    common_columns = ['Account ID', 'Name', 'Status', 'Address', 'City', 'State', 'Zip', 'Email', 'Phone', 'FDA', 'FDH']  # Adjust these based on actual columns
    arlington_df = arlington_df[common_columns]
    mckinney_df = mckinney_df[common_columns]
    rockwall_df = rockwall_df[common_columns]

    combined_df = pd.concat([arlington_df, mckinney_df, rockwall_df], ignore_index=True)
    combined_df.to_excel('combined_address_details.xlsx', index=False)
