# backend/features.py
import re
from collections import Counter
import math
import difflib  # Built-in Python tool to check word similarity

def extract_features(url):
    """
    Extract 17 structural features from a URL.
    Includes a smart typosquatting check for look-alike domains.
    """
    features = []
    
    # Normalize the URL string
    url_clean = str(url).strip().lower()
    url_clean = url_clean.replace('https://', '').replace('http://', '')
    if url_clean.startswith('www.'):
        url_clean = url_clean[4:]
    if url_clean.endswith('/'):
        url_clean = url_clean[:-1]

    # --- Feature Extraction ---
    
    # 1. URL Length
    url_length = len(url_clean)
    features.append(url_length)
    
    # 2. Number of dots
    num_dots = url_clean.count('.')
    features.append(num_dots)
    
    # 3. Number of hyphens
    num_hyphens = url_clean.count('-')
    features.append(num_hyphens)
    
    # 4. Number of underscores
    num_underscores = url_clean.count('_')
    features.append(num_underscores)
    
    # 5. Number of slashes
    num_slashes = url_clean.count('/')
    features.append(num_slashes)
    
    # 6. Number of question marks
    num_question_marks = url_clean.count('?')
    features.append(num_question_marks)
    
    # 7. Number of equals signs
    num_equals = url_clean.count('=')
    features.append(num_equals)
    
    # 8. Number of digits
    num_digits = sum(c.isdigit() for c in url_clean)
    features.append(num_digits)
    
    # 9. Number of letters
    num_letters = sum(c.isalpha() for c in url_clean)
    features.append(num_letters)
    
    # 10. Ratio of digits to length
    digit_ratio = num_digits / url_length if url_length > 0 else 0
    features.append(digit_ratio)
    
    # 11. Has "@" symbol
    has_at_symbol = 1 if '@' in url_clean else 0
    features.append(has_at_symbol)
    
    # 12. Has IP address
    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url_clean) else 0
    features.append(has_ip)
    
    # 13. Number of subdomains
    domain_part = url_clean.split('/')[0]
    domain_parts = domain_part.split('.')
    num_subdomains = len(domain_parts) - 2 if len(domain_parts) > 2 else 0
    features.append(num_subdomains)
    
    # 14. Contains exact common brand names
    brand_names = ['paypal', 'amazon', 'google', 'facebook', 'apple', 'microsoft', 'netflix', 'bank']
    contains_brand = 1 if any(brand in url_clean for brand in brand_names) else 0
    features.append(contains_brand)
    
    # 15. NEW: Typosquatting / Look-alike Domain Finder
    # Extracts the core name (e.g., "gooogle" from "gooogle.com")
    core_domain = domain_parts[0] if len(domain_parts) > 0 else ""
    
    is_typo = 0
    for brand in brand_names:
        # Calculate how close the domain name is to a real brand (0.0 to 1.0)
        similarity = difflib.SequenceMatcher(None, core_domain, brand).ratio()
        # If it is a close match (above 75%) but NOT the exact brand name, it's a typo scam!
        if 0.75 <= similarity < 1.0:
            is_typo = 1
            break
            
    features.append(is_typo)
    
    # 16. Shortened URL
    shortened_services = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly', 'is.gd', 'qrco.de']
    is_shortened = 1 if any(service in url_clean for service in shortened_services) else 0
    features.append(is_shortened)
    
    # 17. Entropy
    if len(url_clean) > 0:
        freq = Counter(url_clean)
        entropy = -sum((count/len(url_clean)) * math.log2(count/len(url_clean)) for count in freq.values())
        features.append(min(entropy / 8, 1))
    else:
        features.append(0)
    
    return features

def get_feature_names():
    """Return names of all 17 features"""
    return [
        'url_length', 'num_dots', 'num_hyphens', 'num_underscores', 'num_slashes',
        'num_question_marks', 'num_equals', 'num_digits', 'num_letters', 'digit_ratio',
        'has_at_symbol', 'has_ip', 'num_subdomains', 'contains_brand', 'is_typo', 'is_shortened', 'entropy'
    ]