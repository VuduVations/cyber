import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Multiline string containing your CSV formatted data
csv_data = '''Asset ID/Name,Type,Application/Software Name,Version,Vendor,Purchase Cost,Development Cost,Admin Cost,Annual Maintenance Cost,Criticality,Data Sensitivity,Threats,Safeguard Measures,Safeguard Cost,EF,Pre ARO,Post ARO,Pre SLE,Post SLE
CRM001,Software,Salesforce,2023,Salesforce,500,100,50,120,High,High,Data breach; Unauthorized access,Two-factor authentication; Regular software updates,200,0.2,0.1,0.05,100,50
ACC002,Software,QuickBooks Online,2023,Intuit,300,75,40,100,High,High,Malware; Phishing attacks,Antivirus software; Employee training on phishing,150,0.3,0.15,0.07,90,45
INV003,Software,TradeGecko,2023,TradeGecko,200,50,30,80,Medium,Medium,Inventory data manipulation; Unauthorized access,User access control; Regular audits,100,0.25,0.12,0.06,80,40
SCH004,Software,Calendly,2023,Calendly,0,0,20,50,Medium,Low,Denial of Service; Data breach,Cloud-based backups; Use of reputable cloud services,80,0.1,0.05,0.025,60,30
WEB005,Software,WordPress,5.9,WordPress,0,0,25,100,High,Medium,SQL Injection; Cross-site scripting,Regular updates; Security plugins,120,0.4,0.2,0.1,110,55
OFF006,Hardware,Office Computers,N/A,Dell,10000,2000,500,500,High,High,Physical theft; Hardware failure,Physical security; Regular hardware checks,500,0.5,0.25,0.12,5000,2500
NET007,Hardware,Office Router,N/A,Netgear,200,0,10,0,High,High,Unauthorized access; MITM attacks,Firewall; Secure Wi-Fi encryption,180,0.4,0.2,0.1,80,40
OFF008,Hardware,Workstation PCs,N/A,HP,8000,1500,400,400,High,Medium,Malware; Data corruption,Anti-malware software; Data backups,400,0.35,0.175,0.0875,2800,1400
INV022,Software,Inventory Management System,2023,Custom,600,200,100,150,Medium,High,Data manipulation; Unauthorized access,Strong password policies; Encryption,220,0.3,0.15,0.075,180,90
SEC023,Hardware,Security Cameras,N/A,Hikvision,3000,0,50,200,High,Low,Theft; Vandalism,Secure installation; Surveillance monitoring,250,0.2,0.1,0.05,600,300'''

# Function to save CSV data to a file
def save_csv_data(csv_data, file_path):
    with open(file_path, "w", encoding="utf-8") as csv_file:
        csv_file.write(csv_data)
    print(f"CSV file has been created at: {file_path}")

# Function to calculate ALE
def calculate_ale(pre_aro, post_aro, pre_sle, post_sle):
    ale_pre = pre_aro * pre_sle
    ale_post = post_aro * post_sle
    return ale_pre, ale_post

# Function to update DataFrame with CBA metrics
def update_cba_metrics(df):
    df['ALE_Pre'] = df['Pre ARO'] * df['Pre SLE']
    df['ALE_Post'] = df['Post ARO'] * df['Post SLE']
    df['ACS'] = df['Annual Maintenance Cost'] + df['Safeguard Cost']
    df['Savings'] = df['ALE_Pre'] - df['ALE_Post']
    df['Net Savings'] = df['Savings'] - df['ACS']
    df['Decision'] = np.where(df['Net Savings'] > 0, 'Go', 'No Go')
    return df

# Function to plot CBA metrics
def plot_cba_metrics(df):
    sns.set_style("whitegrid")
    custom_palette = {'Go': 'green', 'No Go': 'red'}
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 12))
    parameters = ['EF', 'Safeguard Cost', 'Pre ARO', 'Post ARO', 'Pre SLE', 'Post SLE', 'ALE_Pre', 'ALE_Post']

    for i, parameter in enumerate(parameters):
        row = i // 3
        col = i % 3
        ax = axes[row, col]
        sns.barplot(x='Asset ID/Name', y=parameter, data=df, hue='Decision', palette=custom_palette, ax=ax)
        ax.set_title(f'{parameter} by Asset')
        ax.set_xlabel('Asset ID/Name')
        ax.set_ylabel(parameter)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.legend(title='Decision')

    plt.tight_layout()
    plt.show()

# Main execution
csv_file_path = "/content/updated_cba_security_controls.csv"
save_csv_data(csv_data, csv_file_path)

# Load the CSV into a DataFrame
df = pd.read_csv(csv_file_path)
df = update_cba_metrics(df)

# Display the updated DataFrame
print(df.head(15))

# Plot the CBA metrics
plot_cba_metrics(df)
