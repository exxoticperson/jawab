# Jawab Validation & Enrichment Script (PowerShell)

$workspace = "C:\Users\x\Downloads\Creating a Skill Using Skill-Creator and Agent Mode (1)"
$inputPath = "$workspace\Master_Lead_Database_v2\01_CLEANED_READY_TO_SEND.csv"
$outputPath = "$workspace\Master_Lead_Database_v2\01_VALIDATED_ENRICHED.csv"

if (-not (Test-Path $inputPath)) { Write-Host "Input file not found."; exit }

$leads = Import-Csv -Path $inputPath

foreach ($lead in $leads) {
    # 1. Digital Presence Validation (Simulated Network Check)
    $webStatus = "Unknown"
    if ($lead.Website -ne "") {
        try {
            # Low timeout for speed
            Invoke-WebRequest -Uri $lead.Website -Method Head -TimeoutSec 2 -ErrorAction Stop
            $webStatus = "Active"
        } catch {
            $webStatus = "Inactive/Error"
        }
    }
    $lead | Add-Member -MemberType NoteProperty -Name "Website Status" -Value $webStatus -Force

    # 2. Instagram Direct Link (Phase 3)
    if ($lead."Instagram Handle" -match "^@(.+)") {
        $handle = $matches[1]
        $lead | Add-Member -MemberType NoteProperty -Name "IG Direct Link" -Value "https://instagram.com/$handle" -Force
    } else {
        $lead | Add-Member -MemberType NoteProperty -Name "IG Direct Link" -Value "" -Force
    }

    # 3. Pain Signal Enrichment (Phase 3)
    # If the current signal is "SKIP" or empty, generate a logical angle
    if ($lead."Pain Signal" -match "SKIP|^$" -or $null -eq $lead."Pain Signal") {
        $rating = [float]$lead."Google Rating"
        $reviews = [int]$lead."Review Count"
        
        if ($reviews -gt 300) {
            $lead."Pain Signal" = "High volume ($reviews reviews) likely leads to missed calls during peak hours."
        } elseif ($rating -ge 4.9 -and $reviews -gt 50) {
            $lead."Pain Signal" = "Premium reputation ($rating rating) - high patient expectations for instant response."
        } else {
            $lead."Pain Signal" = "Active clinic - potential for missed lead recovery via WhatsApp."
        }
    }

    # 4. ICP Scoring (Phase 4 logic)
    $score = 0
    if ([float]$lead."Google Rating" -ge 4.5) { $score++ }
    if ([int]$lead."Review Count" -gt 100) { $score++ }
    if ($lead."Instagram Handle" -ne "") { $score++ }
    $lead."ICP Score" = $score
}

$leads | Export-Csv -Path $outputPath -NoTypeInformation -Encoding utf8
Write-Host "Phase 2 & 3 Validation/Enrichment Complete."
