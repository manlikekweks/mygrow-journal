import os
import json
from openai import OpenAI

def analyze_spiritual_journal(journal_text):
    """Analyze journal text using DeepSeek API."""
    try:
        # Get API key from environment
        api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            return get_fallback_response("DeepSeek API key not configured")
        
        # Initialize client with DeepSeek endpoint
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"  # DeepSeek endpoint
        )
        
        # Create a prompt for spiritual analysis
        prompt = f"""As a spiritual director, analyze this journal entry and provide guidance:

JOURNAL ENTRY:
"{journal_text}"

Please provide analysis in this EXACT JSON format (no other text):
{{
  "primary_themes": ["theme1", "theme2", "theme3"],
  "emotional_state": ["emotion1", "emotion2"],
  "core_question": "What spiritual question emerges?",
  "key_insight": "Key spiritual insight",
  "bible_passages": [
    {{
      "reference": "Bible reference",
      "text": "Full verse text",
      "why_it_fits": "Brief explanation of relevance"
    }}
  ],
  "practical_steps": ["Actionable step 1", "Actionable step 2", "Actionable step 3"],
  "prayer_starter": "A prayer beginning",
  "encouragement": "Encouraging closing message"
}}

Make the response personal, biblical, and practical."""
        
        # Call DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",  # DeepSeek model
            messages=[
                {"role": "system", "content": "You are a wise spiritual director with deep biblical knowledge. Provide compassionate, practical guidance rooted in Scripture."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        
        # Add timestamp and ensure all fields exist
        result["analysis_timestamp"] = os.path.getmtime(__file__)
        
        # Ensure all required fields exist
        required_fields = ["primary_themes", "emotional_state", "core_question", 
                          "key_insight", "bible_passages", "practical_steps", 
                          "prayer_starter", "encouragement"]
        
        for field in required_fields:
            if field not in result:
                result[field] = get_fallback_response("Missing field")[field]
        
        return result
        
    except json.JSONDecodeError as e:
        return get_fallback_response(f"JSON parsing error: {str(e)[:50]}")
    except Exception as e:
        return get_fallback_response(f"DeepSeek API error: {str(e)[:50]}")

def get_fallback_response(error_msg=""):
    """Provide fallback response when API fails."""
    return {
        "error": error_msg or "AI service temporarily unavailable",
        "primary_themes": ["Faith", "Hope", "Reflection"],
        "emotional_state": ["Seeking", "Open", "Contemplative"],
        "core_question": "What is God revealing to you in this season?",
        "key_insight": "Your willingness to reflect shows spiritual growth.",
        "bible_passages": [
            {
                "reference": "Philippians 4:6-7",
                "text": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
                "why_it_fits": "Offers peace amid uncertainty"
            },
            {
                "reference": "Jeremiah 29:13",
                "text": "You will seek me and find me when you seek me with all your heart.",
                "why_it_fits": "Encourages wholehearted seeking"
            }
        ],
        "practical_steps": [
            "Spend 10 minutes in quiet prayer about what you wrote",
            "Identify one action step from your reflection",
            "Share your insight with a trusted friend this week"
        ],
        "prayer_starter": "God, meet me in my seeking and reveal Your heart to me.",
        "encouragement": "Every moment of reflection brings you closer to God's heart.",
        "is_fallback": True
    }

def get_bible_verse_suggestions(themes):
    """Get Bible verse suggestions based on themes."""
    theme_to_verses = {
        "Anxiety": ["Philippians 4:6-7", "1 Peter 5:7", "Matthew 6:34"],
        "Hope": ["Romans 15:13", "Jeremiah 29:11", "Psalm 42:11"],
        "Faith": ["Hebrews 11:1", "Mark 11:24", "2 Corinthians 5:7"],
        "Peace": ["John 14:27", "Isaiah 26:3", "Colossians 3:15"],
        "Joy": ["Nehemiah 8:10", "Psalm 16:11", "Romans 15:13"],
        "Love": ["1 Corinthians 13:4-7", "John 3:16", "Romans 8:38-39"],
        "Guidance": ["Proverbs 3:5-6", "Psalm 32:8", "Isaiah 30:21"],
        "Strength": ["Isaiah 41:10", "Philippians 4:13", "Psalm 46:1"],
        "Gratitude": ["1 Thessalonians 5:18", "Psalm 107:1", "Colossians 3:17"],
        "Patience": ["Romans 12:12", "James 1:3-4", "Psalm 37:7"]
    }
    
    results = []
    for theme in themes:
        if theme in theme_to_verses:
            for verse in theme_to_verses[theme][:2]:  # Max 2 verses per theme
                results.append({
                    "reference": verse,
                    "theme": theme,
                    "reason": f"Addresses {theme.lower()}"
                })
    
    # If no themes matched, return general verses
    if not results:
        results = [
            {"reference": "Psalm 23:1", "theme": "Provision", "reason": "God's care"},
            {"reference": "Matthew 11:28", "theme": "Rest", "reason": "Jesus' invitation"},
            {"reference": "Romans 8:28", "theme": "Purpose", "reason": "God's plan"}
        ]
    
    return results[:5]  # Return top 5
