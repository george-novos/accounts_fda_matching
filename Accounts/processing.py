import pandas as pd


def package_data(accounts):
    data = []

    for account in accounts:
        account_id = account.get('account_id', 'Unknown')
        service_id = account.get('service_id', 'Unknown')

        package = account.get('package', None)
        package_name = package.get('name', 'Unknown') if package else 'Unknown'

        try:
            service_id = int(service_id)
        except (ValueError, TypeError):
            continue

        if service_id in {49, 50, 51}:
            row_data = {
                "Account ID": account_id,
                "Service ID": service_id,
                "Package Name": package_name,
            }
            data.append(row_data)

    df = pd.DataFrame(data)
    df_cleaned = df.drop_duplicates(subset=['Account ID'])

    print("Number of records saved:", len(df_cleaned))
    return df_cleaned


def mesh_data(accounts):
    data = []

    for account in accounts:
        account_id = account.get('account_id', 'Unknown')
        service_id = account.get('service_id', 'Unknown')

        service = account.get('service', None)
        service_name = service.get('name', 'Unknown') if service else 'Unknown'

        try:
            service_id = int(service_id)
        except (ValueError, TypeError):
            continue

        if service_id in {35}:
            row_data = {
                "Account ID": account_id,
                "Service ID": service_id,
                "Mesh": service_name,
            }
            data.append(row_data)

    df = pd.DataFrame(data)
    df_cleaned = df.drop_duplicates(subset=['Account ID'])

    print("Number of records saved:", len(df_cleaned))
    return df_cleaned


def discount_data(accounts):
    data = []

    for account in accounts:
        account_id = account.get('account_id', 'Unknown')
        service_id = account.get('service_id', 'Unknown')

        service = account.get('service', None)
        service_name = service.get('name', 'Unknown') if service else 'Unknown'

        try:
            service_id = int(service_id)
        except (ValueError, TypeError):
            continue

        if service_id in {119, 120, 121, 122}:
            row_data = {
                "Account ID": account_id,
                "Service ID": service_id,
                "Discounts": service_name,
            }
            data.append(row_data)

    df = pd.DataFrame(data)
    df_cleaned = df.drop_duplicates(subset=['Account ID'])

    print("Number of records saved:", len(df_cleaned))
    return df_cleaned


def auto_pay(accounts):
    data = []

    for account in accounts:
        account_id = account.get('account_id', 'Unknown')
        service_id = account.get('service_id', 'Unknown')

        service = account.get('service', None)
        service_name = service.get('name', 'Unknown') if service else 'Unknown'

        try:
            service_id = int(service_id)
        except (ValueError, TypeError):
            continue

        if service_id in {40}:
            row_data = {
                "Account ID": account_id,
                "Service ID": service_id,
                "Auto-Pay": service_name,
            }
            data.append(row_data)

    df = pd.DataFrame(data)
    df_cleaned = df.drop_duplicates(subset=['Account ID'])

    print("Number of records saved:", len(df_cleaned))
    return df_cleaned


def static_data(accounts):
    data = []

    for account in accounts:
        account_id = account.get('account_id', 'Unknown')
        service_id = account.get('service_id', 'Unknown')

        service = account.get('service', None)
        service_name = service.get('name', 'Unknown') if service else 'Unknown'

        try:
            service_id = int(service_id)
        except (ValueError, TypeError):
            continue

        if service_id in {69}:
            row_data = {
                "Account ID": account_id,
                "Service ID": service_id,
                "Static IP": service_name,
            }
            data.append(row_data)

    df = pd.DataFrame(data)
    df_cleaned = df.drop_duplicates(subset=['Account ID'])

    print("Number of records saved:", len(df_cleaned))
    return df_cleaned


def total_charge(accounts):
    data = []

    for account in accounts:
        account_id = account.get('account_id', 'Unknown')
        charges = account.get('total_debits', 'Unknown')/100

        row_data = {
            "Account ID": account_id,
            "Monthly Total Charges": charges,
        }
        data.append(row_data)

    df = pd.DataFrame(data)
    df_cleaned = df.drop_duplicates(subset=['Account ID'])

    print("Number of records saved:", len(df_cleaned))
    return df_cleaned


def merge_files():
    csv_files = ["accounts.csv", "scheduled_dates.csv", "activation_dates.csv", "autopay.csv", "discounts.csv",
                 "meshes.csv", "packages.csv", "static.csv", "total_charges.csv"]
    sheet_names = ["Sales Report", "Scheduled Date", "Activation Date", "Autopay", "Discounts",
                   "Meshes", "Packages", "Static", "Total Monthly Charges"]

    output_file = "merged_output.xlsx"

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:

        for file, sheet_name in zip(csv_files, sheet_names):
            df = pd.read_csv(file)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    sales_report_df = pd.read_excel('merged_output.xlsx', sheet_name='Sales Report')
    print(sales_report_df.head())

    print(f"CSV files have been successfully merged into {output_file} with 'Sales Report' as the first sheet")



