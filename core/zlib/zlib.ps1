$env:ZLIB_DOMAIN="https://z-lib.gd/"
# Per aggirare il limite di IP, usiamo Tor:
$env:HTTP_PROXY="socks5://127.0.0.1:9050" 

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$zlibExe = Join-Path $scriptDir "zlib.exe"

& $zlibExe @args
