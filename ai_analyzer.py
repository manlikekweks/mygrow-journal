import os
import json
import re
from openai import OpenAI
from datetime import datetime

# Theme mapping for deeper analysis
SPIRITUAL_THEMES = {
    "Faith": ["trust", "belief", "confidence", "assurance", "conviction"],
    "Hope": ["expectation", "anticipation", "optimism", "longing", "aspiration"],
    "Love": ["compassion", "affection", "devotion", "care", "kindness"],
    "Peace": ["calm", "serenity", "tranquility", "harmony", "contentment"],
    "Joy": ["happiness", "delight", "gladness", "cheer", "bliss"],
    "Patience": ["endurance", "perseverance", "steadfastness", "fortitude", "resilience"],
    "Gratitude": ["thankfulness", "appreciation", "recognition", "acknowledgment"],
    "Forgiveness": ["mercy", "pardon", "clemency", "absolution", "reconciliation"],
    "Humility": ["modesty", "meekness", "unpretentiousness", "submission"],
    "Wisdom": ["understanding", "insight", "discernment", "prudence", "knowledge"]
}

BIBLE_BOOKS = {
    "Psalms": "Comfort, prayer, worship",
    "Proverbs": "Wisdom, practical living",
    "Matthew": "Jesus' teachings, Kingdom",
    "John": "Love, relationship with God",
    "Romans": "Doctrine, grace, faith",
    "Philippians": "Joy, contentment",
    "James": "Practical faith, wisdom"
}

def analyze_spiritual_journal(journal_text):
    """Deep spiritual analysis with personalized guidance."""
    try:
        # Get API key
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        if not api_key:
            return get_rich_fallback_response("API key not configured")
        
        # Initialize DeepSeek client
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        # Create comprehensive prompt for deep analysis
        prompt = f"""As a seasoned spiritual director with theological training, provide a DEEP analysis of this journal entry:

JOURNAL ENTRY:
"{journal_text}"

Provide analysis in this EXACT JSON format:
{{
  "analysis_summary": "Brief overall assessment of the spiritual state",
  "primary_themes": ["theme1", "theme2", "theme3", "theme4"],
  "emotional_state": ["emotion1", "emotion2", "emotion3"],
  "core_question": "The central spiritual question emerging",
  "key_insight": "Most important spiritual insight (2-3 sentences)",
  "bible_passages": [
    {{
      "reference": "Scripture reference",
      "text": "Full verse text",
      "why_it_fits": "Detailed explanation of relevance (2-3 sentences)",
      "application": "How to apply this Scripture practically"
    }},
    {{
      "reference": "Second Scripture reference",
      "text": "Full verse text",
      "why_it_fits": "Detailed explanation",
      "application": "Practical application"
    }}
  ],
  "practical_steps": [
    "Specific, actionable step 1",
    "Specific, actionable step 2", 
    "Specific, actionable step 3"
  ],
  "prayer_starter": "A heartfelt prayer paragraph (3-4 sentences)",
  "encouragement": "Personalized encouragement message (2-3 sentences)",
  "growth_areas": ["Area 1 for growth", "Area 2 for growth"],
  "scriptural_promise": "A specific Bible promise that applies"
}}

Guidelines:
1. Be psychologically astute and spiritually deep
2. Identify both surface and underlying themes
3. Provide SPECIFIC Bible passages with full context
4. Make practical steps CONCRETE and doable
5. Prayer should be authentic and heartfelt
6. Insight should be transformative, not just observational
7. Connect emotions to spiritual truths"""
        
        # Call DeepSeek with more tokens for deeper analysis
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system", 
                    "content": """You are a wise, experienced spiritual director with 30 years of counseling experience. 
                    You combine psychological insight with deep biblical wisdom. You notice subtle spiritual patterns 
                    and provide transformative, practical guidance. Your responses are compassionate yet challenging, 
                    always pointing toward spiritual growth and deeper relationship with God."""
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,  # Slightly higher for more creative insights
            max_tokens=1200,  # More tokens for deeper analysis
            response_format={"type": "json_object"}
        )
        
        # Parse and enhance the response
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        
        # Add metadata and enhance
        result = enhance_analysis(result, journal_text)
        
        return result
        
    except json.JSONDecodeError as e:
        return get_rich_fallback_response(f"JSON error: {str(e)[:50]}")
    except Exception as e:
        return get_rich_fallback_response(f"API error: {str(e)[:50]}")

def enhance_analysis(result, journal_text):
    """Add additional insights and structure to the analysis."""
    
    # Add analysis metadata
    result["analysis_timestamp"] = datetime.now().isoformat()
    result["journal_length"] = len(journal_text)
    result["word_count"] = len(journal_text.split())
    
    # Detect spiritual themes from text
    detected_themes = detect_themes(journal_text)
    if detected_themes:
        result["detected_themes"] = detected_themes
    
    # Add reflection questions based on themes
    if "primary_themes" in result:
        result["reflection_questions"] = generate_reflection_questions(result["primary_themes"])
    
    # Add weekly practice suggestion
    result["weekly_practice"] = generate_weekly_practice(result.get("primary_themes", []))
    
    # Ensure all fields exist
    default_structure = {
        "analysis_summary": "A spiritual journey unfolding",
        "primary_themes": ["Reflection", "Growth"],
        "emotional_state": ["Contemplative"],
        "core_question": "What is God inviting you into?",
        "key_insight": "Your openness creates space for transformation.",
        "bible_passages": [
            {
                "reference": "Philippians 1:6",
                "text": "Being confident of this, that he who began a good work in you will carry it on to completion until the day of Christ Jesus.",
                "why_it_fits": "God is continually at work in your spiritual journey.",
                "application": "Trust the process of your growth."
            }
        ],
        "practical_steps": [
            "Reflect on this analysis for 5 minutes",
            "Choose one step to implement this week",
            "Share an insight with someone"
        ],
        "prayer_starter": "God, meet me in this reflection and guide my steps forward.",
        "encouragement": "Your spiritual attention is bearing fruit.",
        "growth_areas": ["Self-awareness", "Practical application"],
        "scriptural_promise": "Jeremiah 29:13 - You will seek me and find me when you seek me with all your heart."
    }
    
    for key, default in default_structure.items():
        if key not in result:
            result[key] = default
    
    return result

def detect_themes(text):
    """Detect spiritual themes from journal text."""
    text_lower = text.lower()
    detected = []
    
    for theme, keywords in SPIRITUAL_THEMES.items():
        for keyword in keywords:
            if keyword in text_lower:
                if theme not in detected:
                    detected.append(theme)
                break
    
    return detected[:5]  # Return top 5 themes

def generate_reflection_questions(themes):
    """Generate deep reflection questions based on themes."""
    questions = []
    
    theme_questions = {
        "Faith": [
            "What is God asking you to trust Him with right now?",
            "Where have you seen evidence of God's faithfulness recently?"
        ],
        "Hope": [
            "What future are you hoping for? How does God fit into that?",
            "What anchors your hope when circumstances are difficult?"
        ],
        "Love": [
            "How are you experiencing God's love in this season?",
            "Where is God inviting you to love more freely?"
        ],
        "Peace": [
            "What disturbs your peace, and what restores it?",
            "How can you create space for God's peace daily?"
        ],
        "Gratitude": [
            "What hidden blessings can you thank God for today?",
            "How does gratitude change your perspective?"
        ]
    }
    
    for theme in themes:
        if theme in theme_questions:
            questions.extend(theme_questions[theme])
    
    # Add general reflection questions
    general_questions = [
        "What is the most important thing God is saying to you through this?",
        "How does this connect to your broader spiritual journey?",
        "What one action would most honor God in this situation?"
    ]
    
    questions.extend(general_questions)
    return questions[:5]  # Return top 5 questions

def generate_weekly_practice(themes):
    """Suggest a weekly spiritual practice based on themes."""
    practices = {
        "Faith": "Practice releasing one worry to God each day this week.",
        "Hope": "Write down three hopes and pray over them each morning.",
        "Love": "Perform one intentional act of kindness daily.",
        "Peace": "Spend 5 minutes in silence with God each day.",
        "Gratitude": "Keep a daily gratitude journal with three entries.",
        "Forgiveness": "Pray for someone who has hurt you each day.",
        "Patience": "Practice waiting gracefully in one situation daily."
    }
    
    for theme in themes:
        if theme in practices:
            return practices[theme]
    
    return "Spend 10 minutes daily reflecting on God's presence in your life."

def get_rich_fallback_response(error_msg=""):
    """Provide substantial fallback response when API fails."""
    return {
        "error": error_msg or "Deep spiritual insights temporarily unavailable",
        "analysis_summary": "A moment of spiritual reflection and seeking",
        "primary_themes": ["Seeking", "Growth", "Transformation"],
        "emotional_state": ["Open", "Reflective", "Hopeful"],
        "core_question": "What is God cultivating in your spirit through this season?",
        "key_insight": "Your willingness to engage in spiritual reflection is itself a sign of growth. The very act of seeking creates space for God to work.",
        "bible_passages": [
            {
                "reference": "Psalm 139:23-24",
                "text": "Search me, God, and know my heart; test me and know my anxious thoughts. See if there is any offensive way in me, and lead me in the way everlasting.",
                "why_it_fits": "This prayer invites God's searching and guidance—exactly what spiritual reflection accomplishes.",
                "application": "Pray this Psalm as you reflect on your journal entry."
            },
            {
                "reference": "James 1:5",
                "text": "If any of you lacks wisdom, you should ask God, who gives generously to all without finding fault, and it will be given to you.",
                "why_it_fits": "Your seeking wisdom through reflection aligns with God's promise to provide understanding.",
                "application": "Ask God specifically for wisdom about what you've written."
            }
        ],
        "practical_steps": [
            "Re-read your journal entry and underline one phrase that stands out. Sit with it for 2 minutes.",
            "Share one insight from your reflection with a trusted friend this week.",
            "Return to this analysis in 3 days and note what has shifted in your understanding."
        ],
        "prayer_starter": "God of all wisdom, meet me in this moment of reflection. Search my heart as I've searched my thoughts. Give me eyes to see what You see, courage to face what needs facing, and grace to receive what You're offering. Guide me into deeper understanding and faithful living.",
        "encouragement": "The path of spiritual growth is rarely linear. Each moment of honest reflection, each prayer uttered, each Scripture pondered—these are stones paving the way forward. You are exactly where you need to be.",
        "growth_areas": ["Self-awareness", "Scriptural application", "Prayer consistency"],
        "scriptural_promise": "Proverbs 2:3-5 - 'Indeed, if you call out for insight and cry aloud for understanding, and if you look for it as for silver and search for it as for hidden treasure, then you will understand the fear of the Lord and find the knowledge of God.'",
        "reflection_questions": [
            "What one word summarizes this season for you?",
            "How is God challenging or comforting you right now?",
            "What next step is emerging from this reflection?"
        ],
        "weekly_practice": "Set aside 10 minutes daily to sit quietly with God, inviting Him to speak to what you've written.",
        "is_fallback": True
    }

def get_bible_verse_suggestions(themes):
    """Get substantial Bible verse suggestions with explanations."""
    theme_verses = {
        "Faith": [
            {"reference": "Hebrews 11:1", "theme": "Faith", "reason": "Defines faith as confidence in what we hope for"},
            {"reference": "Mark 9:24", "theme": "Faith", "reason": "The honest prayer: 'I do believe; help me overcome my unbelief!'"}
        ],
        "Hope": [
            {"reference": "Romans 15:13", "theme": "Hope", "reason": "God as the source of hope that overflows"},
            {"reference": "Jeremiah 29:11", "theme": "Hope", "reason": "God's plans for welfare and future"}
        ],
        "Love": [
            {"reference": "1 Corinthians 13:4-7", "theme": "Love", "reason": "The definitive description of love's character"},
            {"reference": "1 John 4:18", "theme": "Love", "reason": "Perfect love drives out fear"}
        ],
        "Peace": [
            {"reference": "Philippians 4:6-7", "theme": "Peace", "reason": "The peace that guards hearts and minds"},
            {"reference": "John 14:27", "theme": "Peace", "reason": "Jesus' gift of peace, different from the world's"}
        ],
        "Anxiety": [
            {"reference": "1 Peter 5:7", "theme": "Anxiety", "reason": "Cast all your anxiety on God"},
            {"reference": "Matthew 6:25-34", "theme": "Anxiety", "reason": "Jesus' teaching on worry and trust"}
        ],
        "Guidance": [
            {"reference": "Proverbs 3:5-6", "theme": "Guidance", "reason": "Trust and acknowledgment leading to straight paths"},
            {"reference": "Psalm 32:8", "theme": "Guidance", "reason": "God's promise to instruct and teach"}
        ]
    }
    
    results = []
    for theme in themes:
        if theme in theme_verses:
            results.extend(theme_verses[theme])
    
    # If no themes matched, provide general substantial verses
    if not results:
        results = [
            {"reference": "Psalm 23:1-3", "theme": "Provision", "reason": "God's shepherding care through all of life"},
            {"reference": "Romans 8:38-39", "theme": "Security", "reason": "Nothing can separate us from God's love"},
            {"reference": "2 Corinthians 12:9", "theme": "Grace", "reason": "God's strength perfected in weakness"},
            {"reference": "Philippians 4:13", "theme": "Strength", "reason": "Christ as the source of strength for all things"},
            {"reference": "Isaiah 41:10", "theme": "Courage", "reason": "God's promise of presence and strengthening"}
        ]
    
    return results[:5]  # Return top 5