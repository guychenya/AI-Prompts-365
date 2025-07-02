#!/usr/bin/env python3
"""
AI Prompt Directory Generator
Scans all cloned prompt repositories and generates a unified JSON database
"""

import os
import json
import csv
import re
from pathlib import Path

# Base directory containing all repositories
REPOS_DIR = "/Users/guychenya/Documents/GitHub-Repos"
OUTPUT_FILE = "/Users/guychenya/Documents/GitHub-Repos/AI-Prompts-365/AI-Prompt-Directory/prompts_data.json"

def clean_text(text):
    """Clean and format text content"""
    if not text:
        return ""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def extract_prompts_from_csv(csv_path, repo_name):
    """Extract prompts from CSV files (awesome-chatgpt-prompts format)"""
    prompts = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'act' in row and 'prompt' in row:
                    prompts.append({
                        'title': clean_text(row['act']),
                        'description': clean_text(row['prompt']),
                        'source': repo_name,
                        'type': 'role-play' if row.get('for_devs') == 'FALSE' else 'development'
                    })
    except Exception as e:
        print(f"Error reading CSV {csv_path}: {e}")
    return prompts

def extract_prompts_from_md(md_path, repo_name):
    """Extract prompts from Markdown files"""
    # Skip README files
    if md_path.stem.lower() == 'readme':
        return []

    prompts = []
    try:
        with open(md_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Extract title from filename or first heading
        title = md_path.stem.replace('-', ' ').replace('_', ' ').title()

        # Try to extract first paragraph as description
        lines = content.split('\n')
        description = ""
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('```'):
                description = clean_text(line)
                break

        if not description:
            description = f"Prompt template for {title}"

        prompts.append({
            'title': title,
            'description': content, # Store the full content
            'source': repo_name,
            'type': 'template'
        })
    except Exception as e:
        print(f"Error reading MD {md_path}: {e}")
    return prompts

def extract_prompts_from_txt(txt_path, repo_name):
    """Extract prompts from text files"""
    prompts = []
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Extract title from filename and path
        title = txt_path.stem.replace('-', ' ').replace('_', ' ').title()
        parent_dir = txt_path.parent.name

        if parent_dir != repo_name:
            title = f"{parent_dir} - {title}"

        prompts.append({
            'title': title,
            'description': content, # Store the full content
            'source': repo_name,
            'type': 'system-prompt'
        })
    except Exception as e:
        print(f"Error reading TXT {txt_path}: {e}")
    return prompts

def categorize_prompts(prompts):
    """Categorize prompts based on content and source"""
    categories = {
        "AI Development Tools": {"icon": "tool", "prompts": []},
        "General Purpose": {"icon": "brain", "prompts": []},
        "Software Development": {"icon": "code", "prompts": []},
        "Marketing & Business": {"icon": "bar-chart-2", "prompts": []},
        "Product Management": {"icon": "clipboard", "prompts": []},
        "User Experience": {"icon": "pen-tool", "prompts": []},
        "System Prompts": {"icon": "settings", "prompts": []},
        "Role Playing": {"icon": "users", "prompts": []},
        "Education & Learning": {"icon": "book-open", "prompts": []},
        "Creative Writing": {"icon": "edit-3", "prompts": []},
    }

    for prompt in prompts:
        title_lower = prompt['title'].lower()
        desc_lower = prompt['description'].lower()
        source_lower = prompt['source'].lower()

        # Categorization logic
        if any(keyword in title_lower or keyword in desc_lower for keyword in
               ['cursor', 'vscode', 'agent', 'devin', 'replit', 'windsurf', 'lovable', 'v0']):
            categories["AI Development Tools"]["prompts"].append(prompt)
        elif any(keyword in title_lower or keyword in desc_lower for keyword in
                ['code', 'programming', 'development', 'browser extension', 'app development']):
            categories["Software Development"]["prompts"].append(prompt)
        elif any(keyword in title_lower or keyword in desc_lower for keyword in
                ['marketing', 'saas', 'social media', 'viral content', 'headline']):
            categories["Marketing & Business"]["prompts"].append(prompt)
        elif any(keyword in title_lower or keyword in desc_lower for keyword in
                ['product', 'requirements', 'vision', 'metrics', 'growth']):
            categories["Product Management"]["prompts"].append(prompt)
        elif any(keyword in title_lower or keyword in desc_lower for keyword in
                ['ux', 'ui', 'design', 'accessibility', 'localization', 'chatbot']):
            categories["User Experience"]["prompts"].append(prompt)
        elif prompt['type'] == 'system-prompt' or 'system' in source_lower:
            categories["System Prompts"]["prompts"].append(prompt)
        elif prompt['type'] == 'role-play' or any(keyword in title_lower for keyword in
                                                 ['act as', 'interviewer', 'teacher', 'assistant']):
            categories["Role Playing"]["prompts"].append(prompt)
        elif any(keyword in title_lower or keyword in desc_lower for keyword in
                ['learn', 'education', 'teacher', 'pronunciation', 'language']):
            categories["Education & Learning"]["prompts"].append(prompt)
        elif any(keyword in title_lower or keyword in desc_lower for keyword in
                ['write', 'writing', 'story', 'creative', 'script']):
            categories["Creative Writing"]["prompts"].append(prompt)
        else:
            categories["General Purpose"]["prompts"].append(prompt)

    # Remove empty categories
    return {k: v for k, v in categories.items() if v["prompts"]}

def scan_repositories():
    """Scan all repositories and extract prompts"""
    all_prompts = []
    repos_dir = Path(REPOS_DIR)

    repo_mappings = {
        'awesome-chatgpt-prompts': 'ChatGPT Prompts',
        'awesome-ai-system-prompts': 'AI System Prompts',
        'system-prompts-and-models-of-ai-tools': 'AI Tools & Models',
        'AI-Prompt-Database': 'Prompt Database',
        'Awesome-Prompt-Engineering': 'Prompt Engineering',
        'awesome-prompts': 'Awesome Prompts',
        'ChatGPT-System-Prompts': 'ChatGPT System'
    }

    for repo_path in repos_dir.iterdir():
        if not repo_path.is_dir() or repo_path.name.startswith('.'):
            continue

        repo_name = repo_mappings.get(repo_path.name, repo_path.name)
        print(f"Processing repository: {repo_name}")

        # Scan for different file types
        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                # Skip non-text files and licenses
                if file_path.suffix.lower() not in ['.csv', '.md', '.txt'] or 'license' in file_path.name.lower():
                    continue

                suffix = file_path.suffix.lower()

                if suffix == '.csv' and 'prompt' in file_path.name.lower():
                    prompts = extract_prompts_from_csv(file_path, repo_name)
                    all_prompts.extend(prompts)
                elif suffix == '.md':
                    prompts = extract_prompts_from_md(file_path, repo_name)
                    all_prompts.extend(prompts)
                elif suffix == '.txt' and 'prompt' in file_path.name.lower():
                    prompts = extract_prompts_from_txt(file_path, repo_name)
                    all_prompts.extend(prompts)

    print(f"Total prompts extracted: {len(all_prompts)}")
    return all_prompts

def main():
    """Main function to generate the prompts database"""
    print("🤖 AI Prompt Directory Generator")
    print("=" * 50)

    # Create output directory if it doesn't exist
    output_dir = Path(OUTPUT_FILE).parent
    output_dir.mkdir(exist_ok=True)

    # Scan repositories and extract prompts
    all_prompts = scan_repositories()

    # Categorize prompts
    categorized_prompts = categorize_prompts(all_prompts)

    # Save to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(categorized_prompts, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Generated prompts database: {OUTPUT_FILE}")
    print(f"📊 Categories: {len(categorized_prompts)}")
    print(f"📝 Total prompts: {sum(len(cat['prompts']) for cat in categorized_prompts.values())}")

    # Print category summary
    print("\n📋 Category Summary:")
    for category, data in categorized_prompts.items():
        print(f"  {data['icon']} {category}: {len(data['prompts'])} prompts")

if __name__ == "__main__":
    main()
