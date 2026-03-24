# Jawab Leads Merge & Consolidation Script (PowerShell)

$workspace = "C:\Users\x\Downloads\Creating a Skill Using Skill-Creator and Agent Mode (1)"
$v2Dir = "$workspace\Master_Lead_Database_v2"
$finalOutput = "$workspace\Master_Lead_Database_v2\01_READY_TO_SEND_TOP30.csv"
$masterOutput = "$workspace\Master_Lead_Database_v2\03_MERGED_MASTER.csv"

$existing = Import-Csv -Path "$v2Dir\01_CLEANED_READY_TO_SEND.csv"
$newLeads = Import-Csv -Path "$v2Dir\02_NEW_LEADS.csv"

# 1. Deduplicate & Combine
$combined = @()
$names = @{}

foreach ($lead in $existing) {
    if (-not $names.ContainsKey($lead."Clinic Name")) {
        $combined += $lead
        $names[$lead."Clinic Name"] = $true
    }
}

foreach ($lead in $newLeads) {
    if (-not $names.ContainsKey($lead."Clinic Name")) {
        $combined += $lead
        $names[$lead."Clinic Name"] = $true
    }
}

# 2. Select Final Top 30
$top30 = $combined | Sort-Object { [int]$_."Review Count" } -Descending | Select-Object -First 30

$top30 | Export-Csv -Path $finalOutput -NoTypeInformation -Encoding utf8

# 3. Create Merged Master
$allCorrected = Import-Csv -Path "$v2Dir\03_RAW_DATABASE_CLEANED.csv"
$master = $top30 + $allCorrected | Select-Object -Unique "Clinic Name"

$master | Export-Csv -Path $masterOutput -NoTypeInformation -Encoding utf8

Write-Host "Phase 6 Consolidation Complete. Final Top 30 generated."
