import sys
import os
import urllib.request
import urllib.parse
import json
import ssl
import re
import subprocess
from bs4 import BeautifulSoup

# Force UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

# SSL bypass context for self-signed or untrusted certs
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def resolve_libgen_ip():
    print("Resolving libgen.li IP using Cloudflare DNS-over-HTTPS...")
    try:
        doh_url = "https://cloudflare-dns.com/dns-query?name=libgen.li&type=A"
        req = urllib.request.Request(doh_url, headers={"Accept": "application/dns-json"})
        with urllib.request.urlopen(req, context=ctx) as r:
            data = json.loads(r.read().decode('utf-8'))
            ips = [ans["data"] for ans in data.get("Answer", []) if ans["type"] == 1]
            if ips:
                print(f"Successfully resolved libgen.li to {ips[0]}")
                return ips[0]
    except Exception as e:
        print(f"Warning DoH resolution failed: {e}. Using fallback IP.")
    return "179.43.167.164"

def fetch_html(url, ip, host):
    target_url = url.replace(host, ip)
    req = urllib.request.Request(target_url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    req.add_header("Host", host)
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        return r.read()

def download_file(url, ip, host, output_path):
    target_url = url.replace(host, ip)
    # Use system curl to handle redirects and SSL certificates correctly
    cmd = [
        "curl.exe", "-k", "-L",
        "-H", f"Host: {host}",
        target_url,
        "-o", output_path
    ]
    # We run subprocess directly, which prints progress output to stdout/stderr
    subprocess.run(cmd, check=True)

def main():
    dest_dir = "downloads"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    libgen_ip = resolve_libgen_ip()
    host = "libgen.li"
    
    books_to_download = [
        {"query": "System Design Interview Alex Xu", "author": "Alex Xu", "preferred_title": "System Design Interview"},
        {"query": "Designing Machine Learning Systems Chip Huyen", "author": "Chip Huyen", "preferred_title": "Designing Machine Learning Systems"},
        {"query": "Fundamentals of Data Engineering Reis Housley", "author": "Reis", "preferred_title": "Fundamentals of Data Engineering"},
        {"query": "Learning Ray Pumperla Oakes", "author": "Pumperla", "preferred_title": "Learning Ray"},
        {"query": "Natural Language Processing with Transformers Tunstall", "author": "Tunstall", "preferred_title": "Natural Language Processing with Transformers"},
        {"query": "Hands-On Large Language Models Alammar", "author": "Alammar", "preferred_title": "Hands-On Large Language Models"},
        {"query": "Introducing MLOps Treveil", "author": "Treveil", "preferred_title": "Introducing MLOps"}
    ]
    
    for book in books_to_download:
        title = book["preferred_title"]
        print(f"\n==================================================")
        print(f"Searching for: {title}")
        
        query_enc = urllib.parse.quote_plus(book["query"])
        search_url = f"https://libgen.li/index.php?req={query_enc}"
        
        try:
            html = fetch_html(search_url, libgen_ip, host)
            soup = BeautifulSoup(html, "html.parser")
            
            table = soup.find("table", {"id": "tablelibgen"})
            if not table:
                print(f"No results table found for {title}.")
                continue
                
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
                
                # Scoring candidate
                score = 0
                
                # Prefer English
                if "english" in row_lang.lower() or not row_lang:
                    score += 10
                
                # Format preferences
                if row_ext in ["pdf", "epub"]:
                    score += 5
                elif row_ext in ["mobi", "azw3"]:
                    score += 2
                    
                # Author match
                author_match = False
                author_parts = book["author"].split()
                for part in author_parts:
                    if part.lower() in row_author.lower():
                        author_match = True
                        break
                
                if author_match:
                    score += 10
                
                candidates.append({
                    "title": row_title,
                    "author": row_author,
                    "ext": row_ext,
                    "size": row_size,
                    "url": ads_link,
                    "score": score
                })
                
            if not candidates:
                print(f"No matching candidates found for {title}.")
                continue
                
            # Sort candidates by score descending
            candidates.sort(key=lambda x: x["score"], reverse=True)
            best = candidates[0]
            print(f"Best Match found:")
            print(f"  Title: {best['title']}")
            print(f"  Author: {best['author']}")
            print(f"  Format: {best['ext'].upper()} | Size: {best['size']}")
            
            # Request ads page to find direct GET link
            ads_url = f"https://libgen.li/{best['url']}" if not best['url'].startswith("http") else best['url']
            print(f"Fetching download keys from gateway...")
            ads_html = fetch_html(ads_url, libgen_ip, host)
            ads_soup = BeautifulSoup(ads_html, "html.parser")
            
            get_link = None
            for a in ads_soup.find_all("a", href=True):
                if "get.php?md5=" in a["href"]:
                    get_link = a["href"]
                    break
                    
            if not get_link:
                print("Could not find direct download link on gateway page.")
                continue
                
            download_url = f"https://libgen.li/{get_link}" if not get_link.startswith("http") else get_link
            
            # Sanitize filename
            clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
            clean_author = re.sub(r'[\\/*?:"<>|]', "", best["author"].split(',')[0])
            filename = f"{clean_title} ({clean_author}).{best['ext']}"
            output_path = os.path.join(dest_dir, filename)
            
            print(f"Downloading to: {output_path}")
            download_file(download_url, libgen_ip, host, output_path)
            print("Download completed successfully!")
            
        except Exception as e:
            print(f"Error processing {title}: {e}")

if __name__ == "__main__":
    main()
