$cookiePath = "C:\Users\gabri\APP\zlib\tor\data\control_auth_cookie"
if (-not (Test-Path $cookiePath)) {
    Write-Host "Tor non è avviato o file cookie non trovato."
    exit
}
$cookieBytes = [System.IO.File]::ReadAllBytes($cookiePath)
$cookieHex = [System.BitConverter]::ToString($cookieBytes) -replace '-',''
$tcp = New-Object System.Net.Sockets.TcpClient("127.0.0.1", 9051)
$stream = $tcp.GetStream()
$writer = New-Object System.IO.StreamWriter($stream)
$reader = New-Object System.IO.StreamReader($stream)
$writer.AutoFlush = $true

$writer.WriteLine("AUTHENTICATE $cookieHex")
$res1 = $reader.ReadLine()
Write-Host "Auth: $res1"

if ($res1 -match "^250") {
    $writer.WriteLine("SIGNAL NEWNYM")
    $res2 = $reader.ReadLine()
    Write-Host "New IP Signal: $res2"
}

$writer.WriteLine("QUIT")
$reader.ReadLine() | Out-Null
$tcp.Close()
