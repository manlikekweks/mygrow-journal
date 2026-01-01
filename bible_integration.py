# bible_integration.py - CLEAN VERSION (NO STREAMLIT)
import requests
import re

def get_bible_verse(verse_ref, version="WEB"):
    """Get text for a specific Bible verse"""
    try:
        # Clean the verse reference
        clean_ref = verse_ref.replace(" ", "%20")
        
        # Fetch from Bible API
        url = f"https://bible-api.com/{clean_ref}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "text" in data:
                # Clean up the text
                text = data["text"]
                # Remove verse numbers
                text = re.sub(r'\d+\s', '', text)
                return text.strip()
    
    except requests.exceptions.Timeout:
        return "The scripture reflection is taking a moment... Try again shortly."
    except Exception as e:
        print(f"⚠️ Bible API error: {e}")
    
    # Fallback verses
    fallback_verses = {
        "John 3:16": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
        "Psalm 23:1": "The Lord is my shepherd, I lack nothing.",
        "Philippians 4:6": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.",
        "Matthew 11:28": "Come to me, all you who are weary and burdened, and I will give you rest.",
        "Jeremiah 29:11": "For I know the plans I have for you,' declares the Lord, 'plans to prosper you and not to harm you, plans to give you hope and a future."
    }
    
    # Try to match the reference
    for ref, text in fallback_verses.items():
        if ref in verse_ref or verse_ref in ref:
            return text
    
    return "The word of God is living and active. May this scripture speak to your heart today."

def get_book_list():
    """Get list of Bible books"""
    try:
        response = requests.get("https://bible-api.com/books")
        if response.status_code == 200:
            data = response.json()
            return [book["name"] for book in data.get("books", [])]
    except Exception as e:
        print(f"⚠️ Books API error: {e}")
    
    # Fallback list
    return [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
        "Ezra", "Nehemiah", "Esther", "Job", "Psalms",
        "Proverbs", "Ecclesiastes", "Song of Solomon",
        "Isaiah", "Jeremiah", "Lamentations", "Ezekiel",
        "Daniel", "Hosea", "Joel", "Amos", "Obadiah",
        "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
        "Haggai", "Zechariah", "Malachi",
        "Matthew", "Mark", "Luke", "John", "Acts",
        "Romans", "1 Corinthians", "2 Corinthians",
        "Galatians", "Ephesians", "Philippians", "Colossians",
        "1 Thessalonians", "2 Thessalonians", "1 Timothy",
        "2 Timothy", "Titus", "Philemon", "Hebrews",
        "James", "1 Peter", "2 Peter", "1 John",
        "2 John", "3 John", "Jude", "Revelation"
    ]

def get_chapter_list(book_name):
    """Get number of chapters in a book"""
    chapter_ranges = {
        "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36, "Deuteronomy": 34,
        "Joshua": 24, "Judges": 21, "Ruth": 4, "1 Samuel": 31, "2 Samuel": 24,
        "1 Kings": 22, "2 Kings": 25, "1 Chronicles": 29, "2 Chronicles": 36,
        "Ezra": 10, "Nehemiah": 13, "Esther": 10, "Job": 42, "Psalms": 150,
        "Proverbs": 31, "Ecclesiastes": 12, "Song of Solomon": 8,
        "Isaiah": 66, "Jeremiah": 52, "Lamentations": 5, "Ezekiel": 48,
        "Daniel": 12, "Hosea": 14, "Joel": 3, "Amos": 9, "Obadiah": 1,
        "Jonah": 4, "Micah": 7, "Nahum": 3, "Habakkuk": 3, "Zephaniah": 3,
        "Haggai": 2, "Zechariah": 14, "Malachi": 4,
        "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21, "Acts": 28,
        "Romans": 16, "1 Corinthians": 16, "2 Corinthians": 13,
        "Galatians": 6, "Ephesians": 6, "Philippians": 4, "Colossians": 4,
        "1 Thessalonians": 5, "2 Thessalonians": 3, "1 Timothy": 6,
        "2 Timothy": 4, "Titus": 3, "Philemon": 1, "Hebrews": 13,
        "James": 5, "1 Peter": 5, "2 Peter": 3, "1 John": 5,
        "2 John": 1, "3 John": 1, "Jude": 1, "Revelation": 22
    }
    
    if book_name in chapter_ranges:
        return list(range(1, chapter_ranges[book_name] + 1))
    return list(range(1, 31))

def get_verse_list(book_name, chapter_number):
    """Get number of verses in a chapter"""
    key_chapters = {
        ("Psalms", 23): 6,
        ("Psalms", 91): 16,
        ("Matthew", 5): 48,
        ("Matthew", 6): 34,
        ("John", 3): 36,
        ("John", 14): 31,
        ("Romans", 8): 39,
        ("1 Corinthians", 13): 13,
        ("Philippians", 4): 23,
    }
    
    key = (book_name, int(chapter_number))
    if key in key_chapters:
        return list(range(1, key_chapters[key] + 1))
    return list(range(1, 31))