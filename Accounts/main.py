from AccountPackage.processing import package_data, mesh_data, discount_data, auto_pay, static_data, merge_files, \
    total_charge
from Connection import client
from Query.accountPackage import fetch_all_jobs
from Query.invoices import fetch_all_jobs_charges

if __name__ == "__main__":
    '''
    packages = fetch_all_jobs(client)
    packages = package_data(packages)
    packages.to_csv('packages.csv', index=False)

    meshes = fetch_all_jobs(client)
    meshes = mesh_data(meshes)
    meshes.to_csv('meshes.csv', index=False)

    discounts = fetch_all_jobs(client)
    discounts = discount_data(discounts)
    discounts.to_csv('discounts.csv', index=False)

    autopay = fetch_all_jobs(client)
    autopay = auto_pay(autopay)
    autopay.to_csv('autopay.csv', index=False)

    static_ip = fetch_all_jobs(client)
    static_ip = static_data(static_ip)
    static_ip.to_csv('static.csv', index=False)
    '''
    #total_charges = fetch_all_jobs_charges(client)
    #total_charges = total_charge(total_charges)
    #total_charges.to_csv('total_charges.csv', index=False)

    merge_files()