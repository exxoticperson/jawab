import os
import sys

try:
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl"])
    import pandas as pd

def create_master_tracker():
    workspace = r"c:\Users\x\Downloads\Creating a Skill Using Skill-Creator and Agent Mode (1)"
    master_dir = os.path.join(workspace, "Master_Lead_Database")
    output_excel = os.path.join(workspace, "Jawab_Master_Lead_Tracker.xlsx")

    csv1 = os.path.join(master_dir, "01_Ready_To_Send_Top30.csv")
    csv2 = os.path.join(master_dir, "02_Enrichment_Backlog.csv")
    csv3 = os.path.join(master_dir, "03_Raw_Database_All.csv")

    try:
        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            if os.path.exists(csv1):
                pd.read_csv(csv1).to_excel(writer, sheet_name="Ready_To_Send_Top30", index=False)
            if os.path.exists(csv2):
                pd.read_csv(csv2).to_excel(writer, sheet_name="Enrichment_Backlog", index=False)
            if os.path.exists(csv3):
                pd.read_csv(csv3).to_excel(writer, sheet_name="Raw_Database_All", index=False)
        print(f"Successfully created Master Excel Tracker at: {output_excel}")
    except Exception as e:
        print(f"Error creating Excel: {e}")

if __name__ == "__main__":
    create_master_tracker()
