# Jawab Quality Filter Script (PowerShell)

$workspace = "C:\Users\x\Downloads\Creating a Skill Using Skill-Creator and Agent Mode (1)"
$inputPath = "$workspace\Master_Lead_Database_v2\01_VALIDATED_ENRICHED.csv"
$outputPath = "$workspace\Master_Lead_Database_v2\01_CLEANED_READY_TO_SEND.csv"

if (-not (Test-Path $inputPath)) { Write-Host "Input file not found."; exit }

$leads = Import-Csv -Path $inputPath

# Filter Logic:
# 1. MUST have an Instagram handle
# 2. ICP Score >= 2
# 3. If website is inactive, MUST have Instagram
$filtered = $leads | Where-Object {
    $_. "Instagram Handle" -ne "" -and
    [int]$_."ICP Score" -ge 2 -and
    ($_. "Website Status" -eq "Active" -or $_. "Instagram Handle" -ne "")
}

# Sort by Review Count descending
$sorted = $filtered | Sort-Object { [int]$_."Review Count" } -Descending

# Select Top 30 (or all if less)
$final = $sorted | Select-Object -First 30

$final | Export-Csv -Path $outputPath -NoTypeInformation -Encoding utf8
Write-Host "Phase 4 Quality Filter Complete. Found $($final.Count) Tier A leads."
