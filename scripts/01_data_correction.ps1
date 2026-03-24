# Jawab Data Correction Script (PowerShell version)

$workspace = "C:\Users\x\Downloads\Creating a Skill Using Skill-Creator and Agent Mode (1)"
$masterDir = "$workspace\Master_Lead_Database"
$outputDir = "$workspace\Master_Lead_Database_v2"

if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir | Out-Null }

$TargetHeaders = @(
    "Clinic Name", "Doctor Name", "City", "Specialty", "Instagram Handle", 
    "Phone Number", "WhatsApp Number", "Website", "Google Rating", 
    "Review Count", "Pain Signal", "ICP Score"
)

function Clean-Phone($p) {
    if ($null -eq $p -or $p -match "SKIP|Not found") { return "" }
    $digits = $p -replace '[^\d]', ''
    if ($digits.Length -eq 9 -and $digits.StartsWith("0")) { return "+971 $($digits.Substring(1,1)) $($digits.Substring(2))" }
    if ($digits.Length -eq 9) { return "+971 $($digits.Substring(0,1)) $($digits.Substring(1))" }
    if ($digits.Length -eq 12 -and $digits.StartsWith("971")) { return "+$($digits.Substring(0,3)) $($digits.Substring(3,1)) $($digits.Substring(4))" }
    return $p
}

function Extract-Mobile($text) {
    if ($text -match '(\+971[\s]?[5][024568][\s]?\d{7})') { return $matches[1] -replace '\s', '' }
    if ($text -match '(05[024568][\s]?\d{7})') { 
        $num = $matches[1] -replace '\s', ''
        return "+971$($num.Substring(1))" 
    }
    return ""
}

function Clean-IG($ig) {
    if ($null -eq $ig -or $ig -match "SKIP|Not found") { return "" }
    if ($ig.StartsWith("@")) { return $ig }
    if ($ig -match 'instagram\.com/([^/?]+)') { return "@$($matches[1])" }
    if ($ig -notmatch '\s' -and $ig.Length -gt 2) { return "@$ig" }
    return ""
}

# 1. Process 01_Ready_To_Send_Top30.csv
$top30Path = "$masterDir\01_Ready_To_Send_Top30.csv"
if (Test-Path $top30Path) {
    $content = Get-Content $top30Path
    $results = New-Object System.Collections.Generic.List[PSObject]
    # Skip header
    for ($i = 1; $i -lt $content.Count; $i++) {
        $line = $content[$i]
        # Very simple comma split, but handle quotes
        $parts = $line -split '(?<s>,)(?=(?:[^"]|"[^"]*")*$)'
        # Remove empty strings from split (due to delimiter capture)
        $parts = $parts | Where-Object { $_ -ne "," } | ForEach-Object { $_.Trim('"').Trim() }

        if ($parts.Count -ge 4) {
             # Mapping based on observation:
             # 0: Clinic, 1: City, 2: Phone, 3: Doctor, 5: IG, 7: Rating, 8: Reviews, 10: Website, 12: Pain/Notes
             $clinic = $parts[0]
             $city = $parts[1]
             $phone = Clean-Phone $parts[2]
             $doctor = if ($parts[3] -match "SKIP") { "" } else { $parts[3] }
             $ig = Clean-IG $parts[5]
             $rating = $parts[7] -replace '[^\d.]', ''
             $reviews = $parts[8] -replace '[^\d]', ''
             $website = if ($parts[10] -match "Not found|SKIP") { "" } else { $parts[10] }
             $notes = if ($parts.Count -gt 12) { $parts[12] } else { "" }
             
             $mobile = Extract-Mobile $notes
             if ($mobile -eq "") { $mobile = Extract-Mobile $line }

             $obj = [PSCustomObject]@{
                "Clinic Name" = $clinic
                "Doctor Name" = $doctor
                "City" = $city
                "Specialty" = ""
                "Instagram Handle" = $ig
                "Phone Number" = $phone
                "WhatsApp Number" = $mobile
                "Website" = $website
                "Google Rating" = $rating
                "Review Count" = $reviews
                "Pain Signal" = $notes
                "ICP Score" = ""
             }
             $results.Add($obj)
        }
    }
    $results | Export-Csv -Path "$outputDir\01_CLEANED_READY_TO_SEND.csv" -NoTypeInformation -Encoding utf8
}

# 2. Process 02_Enrichment_Backlog.csv
$backlogPath = "$masterDir\02_Enrichment_Backlog.csv"
if (Test-Path $backlogPath) {
    $content = Get-Content $backlogPath
    $results = New-Object System.Collections.Generic.List[PSObject]
    for ($i = 1; $i -lt $content.Count; $i++) {
        $parts = $content[$i] -split '(?<s>,)(?=(?:[^"]|"[^"]*")*$)'
        $parts = $parts | Where-Object { $_ -ne "," } | ForEach-Object { $_.Trim('"').Trim() }
        if ($parts.Count -ge 4) {
             # Mapping: 0: Clinic, 2: City, 3: Phone, 5: Specialty
             $obj = [PSCustomObject]@{
                "Clinic Name" = $parts[0]
                "Doctor Name" = ""
                "City" = $parts[2]
                "Specialty" = if ($parts.Count -gt 5) { $parts[5] } else { "" }
                "Instagram Handle" = ""
                "Phone Number" = Clean-Phone $parts[3]
                "WhatsApp Number" = ""
                "Website" = ""
                "Google Rating" = ""
                "Review Count" = ""
                "Pain Signal" = ""
                "ICP Score" = ""
             }
             $results.Add($obj)
        }
    }
    $results | Export-Csv -Path "$outputDir\02_ENRICHMENT_BACKLOG_CLEANED.csv" -NoTypeInformation -Encoding utf8
}

# 3. Process 03_Raw_Database_All.csv
$rawPath = "$masterDir\03_Raw_Database_All.csv"
if (Test-Path $rawPath) {
    $content = Get-Content $rawPath
    $results = New-Object System.Collections.Generic.List[PSObject]
    for ($i = 1; $i -lt $content.Count; $i++) {
        $parts = $content[$i] -split '(?<s>,)(?=(?:[^"]|"[^"]*")*$)'
        $parts = $parts | Where-Object { $_ -ne "," } | ForEach-Object { $_.Trim('"').Trim() }
        if ($parts.Count -ge 4) {
             # Mapping: 0: Clinic, 2: City, 3: Phone
             $obj = [PSCustomObject]@{
                "Clinic Name" = $parts[0]
                "Doctor Name" = ""
                "City" = $parts[2]
                "Specialty" = ""
                "Instagram Handle" = ""
                "Phone Number" = Clean-Phone $parts[3]
                "WhatsApp Number" = ""
                "Website" = ""
                "Google Rating" = ""
                "Review Count" = ""
                "Pain Signal" = ""
                "ICP Score" = ""
             }
             $results.Add($obj)
        }
    }
    $results | Export-Csv -Path "$outputDir\03_RAW_DATABASE_CLEANED.csv" -NoTypeInformation -Encoding utf8
}

Write-Host "Phase 1 Correction Complete."
