import sys
import os
import requests
import json
import ssl
import re
import time
import urllib.parse
import urllib3
from bs4 import BeautifulSoup

# Force UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def resolve_libgen_ip():
    print("Resolving libgen.li IP using Cloudflare DNS-over-HTTPS...")
    try:
        doh_url = "https://cloudflare-dns.com/dns-query?name=libgen.li&type=A"
        r = requests.get(doh_url, headers={"Accept": "application/dns-json"}, verify=False, timeout=10)
        data = r.json()
        ips = [ans["data"] for ans in data.get("Answer", []) if ans["type"] == 1]
        if ips:
            print(f"Successfully resolved libgen.li to {ips[0]}")
            return ips[0]
    except Exception as e:
        print(f"Warning: DoH resolution failed ({e}). Using fallback IP.")
    return "179.43.167.164"

def fetch_html(url, ip, host):
    target_url = url.replace(host, ip)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Host": host
    }
    r = requests.get(target_url, headers=headers, verify=False, timeout=20)
    return r.text

def download_book_task(book, ip, host, dest_dir):
    title = book["preferred_title"]
    print(f"\n==================================================")
    print(f"Searching for: {title}")
    
    query_enc = urllib.parse.quote_plus(book["query"])
    search_url = f"https://libgen.li/index.php?req={query_enc}"
    
    try:
        html = fetch_html(search_url, ip, host)
        soup = BeautifulSoup(html, "html.parser")
        
        table = soup.find("table", {"id": "tablelibgen"})
        if not table:
            print(f"No results table found for: {title}.")
            return False
            
        rows = table.find_all("tr")[1:] # Skip header
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
            
            # Check for ads link containing MD5
            ads_link = None
            for a in row.find_all("a", href=True):
                if "ads.php?md5=" in a["href"]:
                    ads_link = a["href"]
                    break
            
            if not ads_link:
                continue
            
            score = 0
            
            # Prefer English
            if "english" in row_lang.lower() or not row_lang:
                score += 10
            
            # Format preferences
            if row_ext in ["pdf", "epub"]:
                score += 5
            elif row_ext in ["mobi", "azw3"]:
                score += 2
                
            # Author match (strictly prefer matching authors)
            author_match = False
            author_parts = book["author"].split('|')
            for part in author_parts:
                if part.lower() in row_author.lower():
                    author_match = True
                    break
            
            if author_match:
                score += 100
            
            candidates.append({
                "title": row_title,
                "author": row_author,
                "ext": row_ext,
                "size": row_size,
                "url": ads_link,
                "score": score
            })
            
        if not candidates:
            print(f"No matching candidates found for: {title}")
            return False
            
        # Sort candidates by score descending
        candidates.sort(key=lambda x: x["score"], reverse=True)
        best = candidates[0]
        
        print(f"Best match found:")
        print(f"  Title: {best['title']}")
        print(f"  Author: {best['author']}")
        print(f"  Format: {best['ext'].upper()} | Size: {best['size']}")
        
        # Request ads page to find direct GET link
        ads_url = f"https://libgen.li/{best['url']}" if not best['url'].startswith("http") else best['url']
        ads_html = fetch_html(ads_url, ip, host)
        ads_soup = BeautifulSoup(ads_html, "html.parser")
        
        get_link = None
        for a in ads_soup.find_all("a", href=True):
            if "get.php?md5=" in a["href"]:
                get_link = a["href"]
                break
                
        if not get_link:
            print(f"Could not find download link for: {title}")
            return False
            
        download_url = f"https://libgen.li/{get_link}" if not get_link.startswith("http") else get_link
        
        # Sanitize filename
        clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
        clean_author = re.sub(r'[\\/*?:"<>|]', "", best["author"].split(',')[0])
        filename = f"{clean_title} ({clean_author}).{best['ext']}"
        output_path = os.path.join(dest_dir, filename)
        
        print(f"Downloading to: {output_path}")
        
        # Step 1: Initial request to get redirect target
        target_url = download_url.replace(host, ip)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Host": host
        }
        r_init = requests.get(target_url, headers=headers, verify=False, allow_redirects=False, timeout=15)
        
        if r_init.status_code in [301, 302, 307]:
            redirect_url = r_init.headers.get("Location")
        else:
            redirect_url = target_url
            
        # Step 2: Download from redirect URL without Host header
        r_file = requests.get(redirect_url, verify=False, stream=True, timeout=60)
        if r_file.status_code == 200:
            total_size = int(r_file.headers.get('Content-Length', 0))
            downloaded = 0
            with open(output_path, "wb") as f:
                for chunk in r_file.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r  Progress: {percent:.1f}% ({downloaded/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB)", end="", flush=True)
                        else:
                            print(f"\r  Progress: {downloaded/(1024*1024):.1f} MB", end="", flush=True)
            print()
            print(f"Download completed successfully!")
            return True
        else:
            print(f"Download failed for {title} (HTTP Status {r_file.status_code})")
            return False
            
    except Exception as e:
        print(f"Processing {title} failed: {e}")
        return False

def main():
    dest_dir = "downloads"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    libgen_ip = resolve_libgen_ip()
    host = "libgen.li"
    
    books_to_download = [
        {"query": "Software Architecture Hard Parts Ford", "author": "Ford|Richards", "preferred_title": "Software Architecture The Hard Parts"},
        {"query": "Data Mesh Dehghani", "author": "Dehghani", "preferred_title": "Data Mesh Delivering Data-Driven Value at Scale"},
        {"query": "Robust Python Viafore", "author": "Viafore", "preferred_title": "Robust Python"},
        {"query": "Database Internals Petrov", "author": "Petrov", "preferred_title": "Database Internals"},
        {"query": "Site Reliability Engineering Google", "author": "Beyer|Google", "preferred_title": "Site Reliability Engineering (SRE) Handbook"},
        {"query": "Enterprise Integration Patterns Hohpe", "author": "Hohpe|Woolf", "preferred_title": "Enterprise Integration Patterns"}
    ]
    
    success_count = 0
    for idx, book in enumerate(books_to_download):
        if idx > 0:
            print("\nSleeping for 5 seconds to avoid CDN rate limiting...")
            time.sleep(5)
            
        res = download_book_task(book, libgen_ip, host, dest_dir)
        if res:
            success_count += 1
            
    print(f"\nAll downloads finished! {success_count}/{len(books_to_download)} books completed successfully.")

if __name__ == "__main__":
    main()
