import os
import re
import json
from bs4 import BeautifulSoup
from collections import defaultdict

def audit_repo(repo_path):
    issues_report = defaultdict(list)
    
    # Ensure the path exists
    if not os.path.exists(repo_path):
        print(f"Error: The path '{repo_path}' does not exist.")
        print("Please make sure you are in the correct directory and the repo folder name is correct.")
        return

    for root, dirs, files in os.walk(repo_path):
        # Skip build folders and dependencies
        if any(skip in root for skip in ['node_modules', '.next', 'dist', '.git', 'venv', 'env']):
            continue
            
        for file in files:
            # Added .js for React/Next.js components
            if file.endswith(('.html', '.htm', '.php', '.jsx', '.tsx', '.js')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f, 'html.parser')
                except Exception:
                    continue
                
                page_issues = []
                
                # 1. H1 Audit
                h1s = soup.find_all('h1')
                if len(h1s) == 0: page_issues.append("Missing H1 tag")
                elif len(h1s) > 1: page_issues.append(f"Multiple H1s ({len(h1s)})")
                
                # 2. Meta Description
                meta_desc = soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
                if not meta_desc or not meta_desc.get('content', '').strip():
                    page_issues.append("Missing Meta Description")
                    
                # 3. Image Audit
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    alt = img.get('alt', '')
                    
                    if not alt.strip():
                        page_issues.append(f"IMG missing alt: {src}")
                    elif len(alt) < 15:
                        page_issues.append(f"Generic alt text ('{alt}') on {src}")
                        
                    if not any(src.lower().endswith(ext) for ext in ['.webp', '.avif', '.svg']) and not src.startswith('data:'):
                        page_issues.append(f"Legacy image format: {src}")
                        
                # 4. Schema Audit
                has_schema = False
                for script in soup.find_all('script', type='application/ld+json'):
                    try:
                        data = json.loads(script.string)
                        if isinstance(data, dict) and 'LocalBusiness' in str(data.get('@type', '')):
                            has_schema = True
                    except: pass
                if not has_schema:
                    page_issues.append("Missing LocalBusiness Schema")
                    
                # 5. Internal Linking
                internal_links = [a.get('href') for a in soup.find_all('a') if a.get('href', '').startswith('/')]
                if len(internal_links) < 3:
                    page_issues.append(f"Low internal linking ({len(internal_links)} links)")
                    
                if page_issues:
                    issues_report[file_path] = page_issues

    # Print summary
    total_issues = sum(len(v) for v in issues_report.values())
    print(f"\n✅ Scan complete. Found {total_issues} issues across {len(issues_report)} files.\n")
    for path, issues in list(issues_report.items())[:10]: 
        print(f"📄 {path}:")
        for issue in issues: print(f"  ❌ {issue}")
    if len(issues_report) > 10:
        print(f"\n... and {len(issues_report) - 10} more files with issues.")

if __name__ == "__main__":
    # CHANGE THIS PATH if your repo is named something else!
    audit_repo('') 
