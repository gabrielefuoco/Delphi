$books = @(
    @{Title="Architecture Patterns with Python"; Author="Percival|Gregory"}
    @{Title="Kubernetes: Up and Running"; Author="Burns|Beda|Hightower"}
    @{Title="System Design Interview"; Author="Alex Xu"}
    @{Title="Designing Machine Learning Systems"; Author="Chip Huyen"}
    @{Title="Fundamentals of Data Engineering"; Author="Reis|Housley"}
    @{Title="Learning Ray"; Author="Pumperla|Oakes|Liaw"}
    @{Title="Natural Language Processing with Transformers"; Author="Tunstall|Werra|Wolf"}
    @{Title="Hands-On Large Language Models"; Author="Alammar|Grootendorst"}
    @{Title="Introducing MLOps"; Author="Treveil|Dataiku"}
)

$sessionFile = "$env:USERPROFILE\.config\zlib\session.json"
$userId = ""
$userKey = ""
if (Test-Path $sessionFile) {
    $session = Get-Content $sessionFile | ConvertFrom-Json
    $userId = $session.cookies.remix_userid
    $userKey = $session.cookies.remix_userkey
}

foreach ($b in $books) {
    Write-Host "`n================================================="
    Write-Host "Searching for: $($b.Title)"
    $titleEnc = [uri]::EscapeDataString($b.Title)
    $res = curl.exe -sL -x socks5://127.0.0.1:9050 -H "remix-userid: $userId" -H "remix-userkey: $userKey" -d "message=$titleEnc" "https://z-lib.sk/eapi/book/search"
    $json = $res | ConvertFrom-Json

    $candidateIds = @()
    if ($json.success -eq 1 -and $json.books) {
        foreach ($book in $json.books) {
            if ($book.deleted -eq 0 -and $book.author -match $b.Author) {
                if ($book.href -match "/book/([A-Za-z0-9]+)/") {
                    $candidateIds += $matches[1]
                }
            }
        }
    }

    if ($candidateIds.Length -eq 0) {
        Write-Host "No matching available book found for $($b.Title)."
        continue
    }

    $bookSuccess = $false
    foreach ($targetId in $candidateIds) {
        if ($bookSuccess) { break }
        
        Write-Host "Trying candidate ID: $targetId"
        $retries = 0
        $success = $false
        
        while (-not $success -and $retries -lt 3) {
            Write-Host "Downloading $targetId (Attempt $($retries+1)/3)..."
            
            $job = Start-Job -ScriptBlock {
                param($id)
                Set-Location "c:\Users\gabri\APP\zlib\zlib-cli"
                .\zlib.ps1 download $id --dir ./downloads 2>&1
            } -ArgumentList $targetId
            
            $finished = Wait-Job $job -Timeout 90
            
            if ($finished) {
                $output = Receive-Job $job
                Remove-Job $job
                $outStr = $output -join "`n"
                
                if ($outStr -match "Daily download limit reached" -or $outStr -match "Too Many Requests") {
                    Write-Host "Limit reached! Rotating IP..."
                    .\rotate-ip.ps1
                    Start-Sleep 5
                    $retries++
                } elseif ($outStr -match "Failed to download" -or $outStr -match "Error") {
                    Write-Host "Download failed cleanly. Moving to next candidate or retry..."
                    $retries++
                } else {
                    Write-Host "Download command completed successfully."
                    $success = $true
                    $bookSuccess = $true
                }
            } else {
                Write-Host "Download hanged! Rotating IP and retrying..."
                Stop-Job $job
                Remove-Job $job
                .\rotate-ip.ps1
                Start-Sleep 5
                $retries++
            }
        }
        
        if (-not $success) {
            Write-Host "Failed to download $targetId after 3 retries. Moving to next candidate ID."
        }
    }
    
    if (-not $bookSuccess) {
        Write-Host "Could not download any candidate for $($b.Title)."
    }
}
Write-Host "All books processed!"
