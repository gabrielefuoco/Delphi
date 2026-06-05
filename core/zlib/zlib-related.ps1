param(
    [Parameter(Mandatory=$true)]
    [string]$BookId
)

$domain = "https://z-lib.gd"
if ($env:ZLIB_DOMAIN) { $domain = $env:ZLIB_DOMAIN }
$sessionFile = "$env:USERPROFILE\.config\zlib\session.json"
$userId = ""
$userKey = ""

if (Test-Path $sessionFile) {
    $session = Get-Content $sessionFile | ConvertFrom-Json
    if ($session.domain) { $domain = $session.domain }
    if ($session.cookies.remix_userid) {
        $userId = $session.cookies.remix_userid
        $userKey = $session.cookies.remix_userkey
    }
}

if ($userId -eq "" -or $userKey -eq "") {
    Write-Host "Errore: Sessione non trovata. Effettua prima il login con la CLI zlib."
    exit
}

$eapiUrl = "$domain/eapi/book/$BookId"
Write-Host "Recupero metadati per il libro: $BookId"
$resMeta = (curl.exe -sL -x socks5://127.0.0.1:9050 -H "remix-userid: $userId" -H "remix-userkey: $userKey" $eapiUrl) -join "`n"
$meta = $resMeta | ConvertFrom-Json

if (-not $meta.success -or $meta.success -eq 0) {
    Write-Host "Errore nel recupero del libro. Risposta: $resMeta"
    exit
}

$id = $meta.book.id
$hash = $meta.book.hash

$eapiSimilarUrl = "$domain/eapi/book/$id/$hash/similar"
Write-Host "Recupero libri correlati da: $eapiSimilarUrl"
$resSimilar = (curl.exe -sL -x socks5://127.0.0.1:9050 -H "remix-userid: $userId" -H "remix-userkey: $userKey" $eapiSimilarUrl) -join "`n"

# API returns an array directly, wait let's check
if ($resSimilar -match '"success":0') {
    Write-Host "Nessun libro correlato o errore: $resSimilar"
    exit
}

$similarObj = $resSimilar | ConvertFrom-Json
$books = $similarObj.books

if ($null -ne $books -and $books.Count -gt 0) {
    Write-Host "`n=== Libri Correlati ==="
    foreach ($book in $books) {
        # The url is like /book/ID/title.html. We can extract the base62 ID.
        $base62Id = ""
        if ($book.url -match "/book/([A-Za-z0-9]+)/") {
            $base62Id = $matches[1]
        }
        Write-Host "- ID: $base62Id | Titolo: $($book.title) | Autore: $($book.author)"
    }
} else {
    Write-Host "Nessun libro correlato trovato."
}
