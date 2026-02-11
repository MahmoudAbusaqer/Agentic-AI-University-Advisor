"""
MSU Data Collector
Collects registration FAQ data from Missouri State University website
"""

import requests
from bs4 import BeautifulSoup
import time

# MSU Registration FAQ URLs
SOURCES = [
    "https://www.missouristate.edu/Registrar/FacultyAndStaff/Advisor-Toolkit.htm",
    "https://outreach.missouristate.edu/registration-services-faq.htm",
    "https://studentaffairs.missouristate.edu/academic-advising-and-program-declaration.htm",
]

def scrape_page(url):
    """Scrape text content from a URL, including image descriptions"""
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract image descriptions and alt text before removing elements
        image_descriptions = []
        for img in soup.find_all('img'):
            alt_text = img.get('alt', '')
            title_text = img.get('title', '')

            # Get surrounding context (figure caption, nearby text)
            parent = img.find_parent(['figure', 'div'])
            caption = ''
            if parent:
                caption_elem = parent.find(['figcaption', 'caption', 'p'])
                if caption_elem:
                    caption = caption_elem.get_text(strip=True)

            # Only add if we have meaningful description
            if alt_text or title_text or caption:
                desc = f"[IMAGE DESCRIPTION: {alt_text or title_text}"
                if caption and caption not in (alt_text, title_text):
                    desc += f" - {caption}"
                desc += "]"
                image_descriptions.append(desc)

        # Remove script, style, and navigation elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Add image descriptions at the end if we found any
        if image_descriptions:
            text += "\n\n--- Visual Content Descriptions ---\n"
            text += "\n".join(image_descriptions)
            text += "\n[NOTE: These are descriptions of images from the original page. For full visual guides, visit the source URL above]"

        return text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def create_knowledge_base():
    """Create knowledge base from MSU sources"""
    print("Starting data collection...")
    print("=" * 80)
    print("IMPORTANT: Only using official MSU sources")
    print("No manual additions - pure source data only")
    print("=" * 80)

    all_content = []
    all_content.append("=" * 80)
    all_content.append("MISSOURI STATE UNIVERSITY - COURSE REGISTRATION KNOWLEDGE BASE")
    all_content.append("=" * 80)
    all_content.append("")

    successful_scrapes = 0
    failed_scrapes = 0

    for url in SOURCES:
        content = scrape_page(url)
        if content and len(content) > 500:  # Only count if we got meaningful content
            all_content.append(f"\n--- Source: {url} ---\n")
            all_content.append(content)
            all_content.append("\n" + "=" * 80 + "\n")
            successful_scrapes += 1
            print(f"✓ Successfully scraped: {len(content)} characters")
        else:
            failed_scrapes += 1
            print(f"✗ Failed or insufficient content")

        # Be polite to the server
        time.sleep(2)

    # Add metadata about sources and boundaries
    all_content.append("\n--- KNOWLEDGE BASE METADATA ---\n")
    all_content.append("""
IMPORTANT INSTRUCTIONS FOR THE AI ASSISTANT:

1. ONLY answer questions based on the information in this knowledge base
2. If the answer is not found in the sources above, respond with:
   "I don't have specific information about that in my knowledge base. For accurate information about [topic], please contact the Office of the Registrar at:
   - Email: Registrar@MissouriState.edu
   - Phone: 417-836-5520
   - Location: Carrington Hall 320
   
   Or visit the Academic Advising and Transfer Center at:
   - Email: Advise@MissouriState.edu
   - Phone: 417-836-5258
   - Location: University Hall 109"

3. When content references images, videos, or screenshots:
   - Describe the steps in text format
   - Use numbered lists for clarity
   - If the visual content is essential and cannot be described adequately, direct the student to the original webpage

4. Always cite the source URL when providing information
5. If information might be outdated, mention when to verify (e.g., "Please verify current deadlines on the Academic Calendar")
6. Never make assumptions or add information not present in the sources
    """)

    # Write to file
    knowledge_base_text = "\n".join(all_content)

    with open("knowledge_base.txt", "w", encoding="utf-8") as f:
        f.write(knowledge_base_text)

    # Validation and statistics
    print("\n" + "=" * 80)
    print("KNOWLEDGE BASE CREATION COMPLETE")
    print("=" * 80)
    print(f"✓ Total characters: {len(knowledge_base_text):,}")
    print(f"✓ Successful scrapes: {successful_scrapes}/{len(SOURCES)}")
    if failed_scrapes > 0:
        print(f"⚠ Failed scrapes: {failed_scrapes}/{len(SOURCES)}")
    print(f"✓ File saved: knowledge_base.txt")

    # Quality checks
    print("\n" + "=" * 80)
    print("QUALITY CHECKS")
    print("=" * 80)

    key_terms = {
        "registration": "Registration information",
        "prerequisite": "Prerequisite handling",
        "DegreeWorks": "DegreeWorks system",
        "advisor": "Advising information",
        "hold": "Registration holds",
    }

    for term, description in key_terms.items():
        if term.lower() in knowledge_base_text.lower():
            print(f"✓ {description} present")
        else:
            print(f"⚠ {description} might be missing")

    if len(knowledge_base_text) < 5000:
        print("\n⚠ WARNING: Knowledge base seems small. Agent may have limited information.")
        print("  Consider adding more source URLs in SOURCES list.")

    print("\n" + "=" * 80)
    print("Ready to use! Run 'python agent.py' to test.")
    print("=" * 80)

    return knowledge_base_text

if __name__ == "__main__":
    create_knowledge_base()