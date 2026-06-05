$torExe = "C:\Users\gabri\APP\zlib\tor\tor\tor.exe"
$torrc = "C:\Users\gabri\APP\zlib\tor\torrc"
Start-Process -FilePath $torExe -ArgumentList "-f", $torrc -WindowStyle Hidden
Write-Host "Tor avviato in background sulla porta 9050 (Controllo: 9051)."
