# Script to group JSONL records by repo field
$filePath = "d:\Downloads\1\Claude-haiku-4.5\v-lkan_25_12_05_case1\repo_metadata.jsonl"
$outputDir = "d:\Downloads\1\Claude-haiku-4.5\v-lkan_25_12_05_case1\output"

# Create output directory if it doesn't exist
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Dictionary to store grouped records by repo
$repoGroups = @{}

# Read and process each line
Get-Content $filePath | ForEach-Object {
    if ([string]::IsNullOrWhiteSpace($_)) { return }
    
    # Parse JSON
    $json = $_ | ConvertFrom-Json
    $repo = $json.repo
    
    # Initialize list for this repo if not exists
    if (-not $repoGroups.ContainsKey($repo)) {
        $repoGroups[$repo] = @()
    }
    
    # Add the full line to the repo group
    $repoGroups[$repo] += $_
}

# Write each group to a separate file
foreach ($repo in $repoGroups.Keys) {
    # Replace / with __ to make valid filename
    $fileName = $repo -replace '/', '__'
    $outputFile = Join-Path $outputDir "$fileName.jsonl"
    
    # Write all lines for this repo to the file
    $repoGroups[$repo] | Set-Content -Path $outputFile
    
    Write-Host "Created $outputFile with $($repoGroups[$repo].Count) record(s)"
}

Write-Host "`nTotal repos: $($repoGroups.Count)"
Write-Host "Output directory: $outputDir"
