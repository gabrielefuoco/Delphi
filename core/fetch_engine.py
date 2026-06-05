import os
import urllib.request
import urllib.parse
import json
import ssl
import re
import subprocess
from bs4 import BeautifulSoup
from typing import Optional

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def _resolve_libgen_ip() -> str:
    print("🌐 Risoluzione IP di libgen.li tramite Cloudflare DNS-over-HTTPS...")
    try:
        doh_url = "https://cloudflare-dns.com/dns-query?name=libgen.li&type=A"
        req = urllib.request.Request(doh_url, headers={"Accept": "application/dns-json"})
        with urllib.request.urlopen(req, context=ctx) as r:
            data = json.loads(r.read().decode('utf-8'))
            ips = [ans["data"] for ans in data.get("Answer", []) if ans["type"] == 1]
            if ips:
                print(f"✅ IP Risolto: {ips[0]}")
                return ips[0]
    except Exception as e:
        print(f"⚠️ Errore risoluzione DoH: {e}. Uso fallback IP.")
    return "179.43.167.164"

def _fetch_html(url: str, ip: str, host: str) -> bytes:
    target_url = url.replace(host, ip)
    req = urllib.request.Request(target_url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    req.add_header("Host", host)
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return r.read()

def download_book(query: str, dest_dir: str = "downloads") -> Optional[str]:
    """Cerca e scarica il miglior libro corrispondente alla query su LibGen."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    libgen_ip = _resolve_libgen_ip()
    host = "libgen.li"
    
    print(f"🔎 Ricerca in corso per: {query}")
    query_enc = urllib.parse.quote_plus(query)
    search_url = f"https://libgen.li/index.php?req={query_enc}"
    
    try:
        html = _fetch_html(search_url, libgen_ip, host)
        soup = BeautifulSoup(html, "html.parser")
        
        table = soup.find("table", {"id": "tablelibgen"})
        if not table:
            print("❌ Nessun risultato trovato.")
            return None
            
        rows = table.find_all("tr")[1:] # Salta header
        candidates = []
        
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 8:
                continue
            
            row_title = cols[0].get_text(strip=True)
            row_author = cols[1].get_text(strip=True)
            row_lang = cols[4].get_text(strip=True)
            row_size = cols[6].get_text(strip=True)
            row_ext = cols[7].get_text(strip=True).lower()
            
            ads_link = None
            for a in row.find_all("a", href=True):
                if "ads.php?md5=" in a["href"]:
                    ads_link = a["href"]
                    break
            
            if not ads_link:
                continue
            
            score = 0
            if "english" in row_lang.lower() or "italian" in row_lang.lower() or not row_lang:
                score += 10
            
            if row_ext in ["pdf", "epub"]:
                score += 5
            elif row_ext in ["mobi", "azw3"]:
                score += 2
                
            query_parts = query.lower().split()
            title_lower = row_title.lower()
            author_lower = row_author.lower()
            matches = sum(1 for p in query_parts if p in title_lower or p in author_lower)
            score += (matches * 2)
            
            candidates.append({
                "title": row_title,
                "author": row_author,
                "ext": row_ext,
                "size": row_size,
                "url": ads_link,
                "score": score
            })
            
        if not candidates:
            print("❌ Nessun candidato valido trovato.")
            return None
            
        candidates.sort(key=lambda x: x["score"], reverse=True)
        best = candidates[0]
        print(f"🎯 Miglior risultato trovato:")
        print(f"   Titolo: {best['title']}")
        print(f"   Autore: {best['author']}")
        print(f"   Formato: {best['ext'].upper()} | Dimensione: {best['size']}")
        
        ads_url = f"https://libgen.li/{best['url']}" if not best['url'].startswith("http") else best['url']
        print("🔗 Estrazione link diretto...")
        ads_html = _fetch_html(ads_url, libgen_ip, host)
        ads_soup = BeautifulSoup(ads_html, "html.parser")
        
        get_link = None
        for a in ads_soup.find_all("a", href=True):
            if "get.php?md5=" in a["href"]:
                get_link = a["href"]
                break
                
        if not get_link:
            print("❌ Impossibile trovare il link di download diretto.")
            return None
            
        download_url = f"https://libgen.li/{get_link}" if not get_link.startswith("http") else get_link
        
        clean_title = re.sub(r'[\\/*?:"<>|]', "", best["title"])[:50].strip()
        clean_author = re.sub(r'[\\/*?:"<>|]', "", best["author"].split(',')[0]).strip()
        filename = f"{clean_title} ({clean_author}).{best['ext']}"
        output_path = os.path.join(dest_dir, filename)
        
        print(f"⬇️ Download in corso in: {output_path}")
        cmd = [
            "curl.exe", "-k", "-L",
            "-H", f"Host: {host}",
            download_url.replace(host, libgen_ip),
            "-o", output_path
        ]
        subprocess.run(cmd, check=True)
        print("✅ Download completato con successo!")
        return output_path
        
    except Exception as e:
        print(f"❌ Errore durante il processo: {e}")
        return None
