$ids = @("PM9WbPd253", "Nr9bGxNwzB", "nXqGyA009m", "l6qBljJx9J", "X69NbLEn9Y", "4Q54V0rxzg")
$jobs = @()

# Ensure downloads directory exists
if (-not (Test-Path ".\downloads")) {
    New-Item -ItemType Directory -Path ".\downloads" | Out-Null
}

foreach ($id in $ids) {
    Write-Host "Avvio download in background per ID: $id"
    $job = Start-Job -ScriptBlock {
        param($bookId)
        Set-Location "c:\Users\gabri\APP\zlib\zlib-cli"
        $output = .\zlib.ps1 download $bookId --dir ./downloads 2>&1
        return "$bookId completato. Output:`n$output"
    } -ArgumentList $id
    $jobs += $job
}

Write-Host "In attesa del completamento dei download contemporanei..."
Wait-Job $jobs | Out-Null

Write-Host "`n=== Risultati dei Download ==="
foreach ($job in $jobs) {
    $result = Receive-Job $job
    Write-Host "Job $($job.Id):"
    Write-Host $result
    Write-Host "---------------------------"
}

# Clean up jobs
Remove-Job $jobs
