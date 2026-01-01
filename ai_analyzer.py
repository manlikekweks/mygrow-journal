# ai_analyzer.py - ENHANCED WITH DEEP PATTERN RECOGNITION (KEEPS DEEP ANALYSIS)
import os
import json

def get_deepseek_client():
    """Get DeepSeek client - handles both single and double quotes."""
    try:
        # Method 1: Environment variable
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        if not api_key:
            # Method 2: Secrets file
            secrets_path = ".streamlit/secrets.toml"
            if os.path.exists(secrets_path):
                with open(secrets_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Find the API key line (handles both single and double quotes)
                for line in content.split('\n'):
                    line = line.strip()
                    if 'DEEPSEEK_API_KEY' in line and '=' in line:
                        # Extract value after =
                        value = line.split('=', 1)[1].strip()
                        
                        # Remove BOTH single and double quotes
                        if (value.startswith("'") and value.endswith("'")) or \
                           (value.startswith('"') and value.endswith('"')):
                            api_key = value[1:-1]  # Remove first and last character
                        else:
                            api_key = value  # No quotes
                        break
        
        if api_key and api_key.startswith('sk-'):
            from openai import OpenAI
            return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        else:
            print(f"⚠️ Invalid or missing API key. Found: '{api_key}'")
            return None
            
    except Exception as e:
        print(f"⚠️ Error getting client: {e}")
        return None

def analyze_spiritual_journal(journal_text):
    """Analyze journal with DEEP PATTERN RECOGNITION and meaningful connections."""
    
    # Generate meaningful fallback themes based on journal content with better pattern recognition
    def get_fallback_themes_and_insights(text):
        """Extract themes and insights from text when AI is unavailable."""
        journal_lower = text.lower()
        
        # Pattern recognition for themes - KEEP DESCRIPTIONS FOR INSIGHT
        theme_patterns = {
            "Gratitude - noticing God's daily gifts": ["thank", "grateful", "appreciate", "blessed", "thankful", "gratitude"],
            "Peace - finding calm in Christ": ["peace", "calm", "still", "quiet", "serene", "tranquil", "anxious", "worried"],
            "Love - experiencing divine affection": ["love", "care", "compassion", "affection", "cherish", "relationship"],
            "Hope - anchoring in God's promises": ["hope", "future", "expect", "anticipate", "tomorrow"],
            "Faith - learning to trust God's character": ["faith", "believe", "trust", "confidence", "rely", "doubt"],
            "Guidance - seeking God's direction": ["guidance", "direction", "path", "wisdom", "counsel", "lost"],
            "Strength - finding power in weakness": ["strength", "strong", "power", "courage", "endurance", "weak"],
            "Forgiveness - receiving and extending grace": ["forgive", "mercy", "pardon", "grace", "absolve", "sorry"],
            "Prayer - cultivating conversation with God": ["pray", "prayer", "ask", "petition", "intercede", "talk to God"],
            "Purpose - discovering God's calling": ["purpose", "calling", "meaning", "mission", "vocation"],
            "Growth - maturing in spiritual understanding": ["grow", "change", "improve", "progress", "develop"],
            "Reflection - thoughtfully processing life": ["reflect", "think", "ponder", "consider", "meditate"],
            "Rest - ceasing from striving": ["rest", "resting", "sabbath", "renew", "refresh"],
            "Identity - understanding who I am in Christ": ["identity", "who am i", "self", "worth", "value"],
            "Transformation - becoming a new creation": ["change", "transform", "new creation", "born again", "renewal"]
        }
        
        # Find matching themes
        themes_found = []
        for theme, keywords in theme_patterns.items():
            if any(keyword in journal_lower for keyword in keywords):
                themes_found.append(theme)
        
        if not themes_found:
            themes_found = ["Spiritual Reflection - considering life's deeper meaning", 
                           "Personal Growth - developing Christ-like character",
                           "Seeking God - longing for deeper connection"]
        
        # Generate insights based on text patterns
        insight_patterns = [
            ("I feel", "Your honest expression of feelings creates space for God to meet you where you are. This vulnerability is the fertile ground where spiritual growth takes root."),
            ("I need", "Recognizing your needs is the first step toward receiving God's provision. His supply often comes through the very acknowledgment of our lack."),
            ("I want", "Desire can be a compass pointing toward what God has placed in your heart. Pay attention to these holy longings."),
            ("I pray", "Prayer connects your heart with God's heart, aligning your desires with His will. This communion transforms both the pray-er and the prayer."),
            ("I hope", "Hope anchors the soul in God's promises, even when circumstances are uncertain. This is not wishful thinking but confident expectation in His character."),
            ("thank", "Gratitude shifts focus from what's missing to what's already been given. This practice rewires the brain to notice God's daily provisions."),
            ("help", "Acknowledging need for help opens the door to God's grace and community support. Our weakness becomes the canvas for His strength."),
            ("try", "Your willingness to try shows faith in action, believing God can work through your efforts. This is the partnership of divine power and human obedience.")
        ]
        
        key_insight = "Your reflections reveal a heart that is open and seeking spiritual growth. This posture of receptivity positions you to receive what God wants to reveal and develop in you."
        for pattern, insight in insight_patterns:
            if pattern in journal_lower:
                key_insight = insight
                break
        
        return themes_found, key_insight
    
    try:
        client = get_deepseek_client()
        
        if client is None:
            # No API client available - return meaningful fallback with pattern recognition
            fallback_themes, fallback_insight = get_fallback_themes_and_insights(journal_text)
            
            return {
                "primary_themes": fallback_themes[:3],  # KEEP DESCRIPTIONS FOR DEPTH
                "emotional_state": ["Reflective - thoughtfully processing life experiences", "Seeking - looking for spiritual understanding"],
                "core_question": "What deeper spiritual patterns is God revealing to me through these reflections, and how are they shaping my journey of transformation?",
                "key_insight": fallback_insight,
                "bible_passages": [
                    {
                        "reference": "Matthew 6:33",
                        "text": "But seek first the kingdom of God and his righteousness, and all these things will be added to you.",
                        "why_it_fits": "Your reflections demonstrate a heart posture that aligns with this kingdom priority. When we genuinely seek God's ways first, our perspective shifts from scarcity to provision, from anxiety to trust. This isn't about religious duty but about relational alignment with how God designed life to work best.",
                        "connection": "The principle here is one of divine economy: when we prioritize spiritual realities, material concerns find their proper place. Your journaling practice itself is an act of seeking first God's kingdom—making space to hear His voice and understand His ways in your life."
                    }
                ],
                "practical_steps": [
                    "Track the recurring themes in your last 3-5 journal entries—what patterns is God emphasizing in this season?",
                    "Identify one specific, small action you can take this week that aligns with the primary spiritual theme emerging in your reflections.",
                    "Share one key insight from your journaling with a trusted spiritual friend—this externalizes internal processing and often brings additional clarity."
                ],
                "prayer_starter": "Lord, as I reflect on these experiences and insights, help me to see with spiritual eyes what You are doing beneath the surface of my life. Teach me to recognize Your patterns, to cooperate with Your work, and to rest in Your timing. Transform my reflections into transformed living.",
                "encouragement": "Your commitment to reflective journaling creates a sacred space for God to speak and for you to listen. This practice itself is a form of worship—an acknowledgment that your story matters to God and that He is actively at work in every detail. Keep creating this space; it is bearing fruit even when you can't immediately see it.",
                "pattern_insights": [
                    "Your reflections show increasing spiritual awareness and the ability to connect daily experiences with eternal truths",
                    "Patterns in your journal reveal God's gentle, persistent guidance working through ordinary moments to produce extraordinary growth"
                ]
            }
        
        # ENHANCED PROMPT for DEEP PATTERN RECOGNITION - KEEPING DEPTH
        system_prompt = """You are a spiritually insightful director with expertise in biblical psychology and pattern recognition.
        Your task is to analyze journal entries and identify DEEP PATTERNS, SPIRITUAL CONNECTIONS, and TRANSFORMATIONAL INSIGHTS.
        
        Analyze this journal entry and provide COMPREHENSIVE, DEEP spiritual guidance focusing on:
        1. PATTERNS: What recurring themes, emotions, or spiritual longings appear beneath the surface?
        2. CONNECTIONS: How do these patterns connect to biblical truths and the ongoing work of spiritual formation?
        3. TRANSFORMATIONAL INSIGHTS: What is God revealing about His character, His work, and the person's spiritual journey?
        
        Return ONLY a JSON object with these exact keys:
        1. "primary_themes": array of 2-3 spiritual themes WITH EXPLANATIONS (e.g., ["New Creation - embracing identity transformation in Christ as described in 2 Corinthians 5:17", "Restful Trust - finding freedom from striving by accepting Jesus' completed work"])
        2. "emotional_state": array of 2-3 emotions WITH CONTEXT (e.g., ["Reassured - experiencing deep comfort from biblical truth about identity", "Peaceful - feeling freedom from pressure and striving"])
        3. "core_question": string - the deepest spiritual question emerging (1-2 thoughtful sentences)
        4. "key_insight": string - profound spiritual insight connecting patterns to growth and transformation (3-4 substantial sentences)
        5. "bible_passages": array of 2-3 objects, each with:
           - "reference": Bible verse (e.g., "2 Corinthians 5:17")
           - "text": The verse text (quote exactly)
           - "why_it_fits": How it specifically addresses their patterns, situation, and spiritual development (3-4 substantial sentences)
           - "connection": The spiritual principle or transformative truth connecting verse to their life (2-3 thoughtful sentences)
        6. "practical_steps": array of 3 actionable, specific steps tied to their patterns
        7. "prayer_starter": string - a prayer responding to their patterns and inviting God's work (3-4 meaningful sentences)
        8. "encouragement": string - words affirming their spiritual journey and God's faithfulness (2-3 substantial sentences)
        9. "pattern_insights": array of 2-3 insights about their spiritual patterns and development
        
        CRITICAL INSTRUCTIONS FOR DEPTH AND INSIGHT:
        - For "primary_themes": Include BOTH the theme name AND a brief explanation (e.g., "Theme - explanation of spiritual significance")
        - For "emotional_state": Include BOTH the emotion AND its spiritual context
        - For "why_it_fits": Provide SUBSTANTIAL explanation connecting the verse to their specific situation and spiritual growth
        - For "key_insight": Offer PROFOUND, TRANSFORMATIONAL insight, not surface-level observations
        - Look for DEEP PATTERNS beneath the surface of their experiences
        - Connect biblical truths SPECIFICALLY to their life context and spiritual development
        - Be COMPASSIONATE, DEEPLY BIBLICAL, and TRANSFORMATIONALLY FOCUSED
        - Write with SUBSTANCE and SPIRITUAL DEPTH
        - Use double quotes for all JSON strings
        - Ensure valid JSON format
        
        The goal is DEEP SPIRITUAL GUIDANCE, not superficial analysis."""
        
        # Truncate journal text if too long (for API limits)
        if len(journal_text) > 3000:
            journal_text = journal_text[:3000] + "... [truncated for length]"
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": journal_text}
            ],
            response_format={"type": "json_object"},
            max_tokens=2000,  # Increased for more substantial analysis
            temperature=0.7
        )
        
        # Get and clean the response
        raw_response = response.choices[0].message.content
        
        # Clean the response - remove any markdown code blocks
        cleaned_response = raw_response.strip()
        
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
        
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        
        cleaned_response = cleaned_response.strip()
        
        # Try to parse the JSON
        try:
            result = json.loads(cleaned_response)
            
            # Validate that we have the required keys WITH SUBSTANCE
            required_keys = ["primary_themes", "emotional_state", "core_question", 
                           "key_insight", "bible_passages", "practical_steps", 
                           "prayer_starter", "encouragement", "pattern_insights"]
            
            for key in required_keys:
                if key not in result:
                    print(f"⚠️ Missing key in AI response: {key}")
                    # Use enhanced fallback for missing key WITH DEPTH
                    themes, insight = get_fallback_themes_and_insights(journal_text)
                    
                    if key == "primary_themes":
                        result[key] = themes[:3]
                    elif key == "emotional_state":
                        result[key] = ["Reflective - thoughtfully processing life experiences and God's work", "Seeking - looking for deeper spiritual understanding and connection"]
                    elif key == "core_question":
                        result[key] = "What deeper work is God doing in my heart through these experiences, and how is He inviting me to participate in my own transformation?"
                    elif key == "key_insight":
                        result[key] = insight
                    elif key == "bible_passages":
                        result[key] = [{
                            "reference": "Philippians 4:6-7",
                            "text": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
                            "why_it_fits": "This passage directly addresses the human tendency toward anxiety while offering a transformative spiritual pattern. The movement from anxiety to peace happens through specific practices: prayer that expresses dependence, petition that names our needs, and thanksgiving that remembers God's faithfulness. This isn't merely a technique but a relational process that guards both heart and mind.",
                            "connection": "The transformative principle here is that peace comes not from changed circumstances but from changed perspective through prayerful engagement with God. Your journaling itself can become a form of this prayerful processing, transforming anxiety into trust."
                        }]
                    elif key == "practical_steps":
                        result[key] = [
                            "Practice the Philippians 4:6-7 pattern this week: when anxious thoughts arise, consciously move through prayer (connection), petition (specific request), and thanksgiving (remembering past faithfulness).",
                            "Review your last 5 journal entries and identify one recurring theme—what might God be emphasizing in this season of your life?",
                            "Share one spiritual insight from your reflections with someone this week—external processing often brings additional clarity and accountability."
                        ]
                    elif key == "prayer_starter":
                        result[key] = "Lord, in the midst of my reflections and experiences, help me to see what You are doing beneath the surface. Teach me to recognize Your patterns in my life, to cooperate with Your transformative work, and to rest in Your good timing and purposes. Transform my understanding as I seek to understand Your ways."
                    elif key == "encouragement":
                        result[key] = "God is actively at work in your life, using every experience—both joyful and challenging—to shape you more into the image of Christ. Your willingness to reflect and process these experiences is itself evidence of His work in you. Keep creating space for this reflection; it is bearing spiritual fruit."
                    elif key == "pattern_insights":
                        result[key] = [
                            "Your reflections demonstrate increasing spiritual maturity—the ability to connect daily experiences with eternal truths and to recognize God's activity in ordinary moments.",
                            "Patterns in your journal reveal God's gentle, persistent guidance, working through both challenges and blessings to produce Christ-like character and deeper dependence on Him."
                        ]
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")
            print(f"Raw response (first 500 chars): {cleaned_response[:500]}")
            
            # Return enhanced fallback on JSON error WITH DEPTH
            themes, insight = get_fallback_themes_and_insights(journal_text)
            
            return {
                "primary_themes": themes[:3],
                "emotional_state": ["Reflective - thoughtfully considering life's experiences and God's work", "Patient - learning to trust in God's timing and purposes"],
                "core_question": "What spiritual patterns and transformative work is God revealing through my journey of reflection and journaling?",
                "key_insight": insight,
                "bible_passages": [
                    {
                        "reference": "Psalm 119:105",
                        "text": "Your word is a lamp for my feet, a light on my path.",
                        "why_it_fits": "God's Word illuminates not only our external circumstances but, more importantly, the internal spiritual patterns and growth happening within us. It shows us the way forward by revealing God's character, promises, and purposes. Your reflective journaling is a way of allowing Scripture to illuminate your personal journey, connecting divine truth with daily experience.",
                        "connection": "The transformative principle is that Scripture provides both direction and illumination for our spiritual journey. It helps us recognize God's patterns in our lives and understand how He is at work shaping us into Christ's image through both Scripture and Spirit-led reflection."
                    }
                ],
                "practical_steps": [
                    "Continue your practice of reflective journaling—this discipline creates space for God to speak and for you to process His work in your life.",
                    "As you review past entries, ask 'What recurring themes or patterns do I see?' and 'How might God be using these patterns for my spiritual growth?'",
                    "Select one biblical principle from your reflections this week and consciously apply it to a specific situation or relationship."
                ],
                "prayer_starter": "Lord, as I reflect on my journey, illuminate the patterns of Your work in my life. Help me to see where You are leading, how You are transforming, and what You are inviting me into. Give me spiritual eyes to recognize Your activity in both ordinary and extraordinary moments, and a heart willing to follow where You lead.",
                "encouragement": "Your commitment to spiritual reflection through journaling is a significant spiritual discipline that positions you to receive God's guidance and recognize His work. This practice itself is transformative, shaping your ability to notice God's presence and activity in your daily life. The very act of reflection is evidence of spiritual growth and sensitivity to the Holy Spirit's work.",
                "pattern_insights": [
                    "Consistent spiritual reflection through journaling develops the capacity to recognize God's patterns of faithfulness and guidance in your life.",
                    "God uses the discipline of reflection to transform your perspective, helping you see His work in all circumstances and developing spiritual discernment and maturity over time."
                ]
            }
        
    except Exception as e:
        print(f"❌ AI Analysis Error: {str(e)[:100]}")
        
        # Return meaningful fallback on any error with pattern recognition AND DEPTH
        themes, insight = get_fallback_themes_and_insights(journal_text)
        
        return {
            "primary_themes": themes[:3],
            "emotional_state": ["Hopeful - looking to the future with expectation of God's continued work", "Patient - learning to trust in God's timing and developmental processes"],
            "core_question": "How can I cultivate greater awareness of God's transformative patterns in my daily life and spiritual journey?",
            "key_insight": "Even when technology has limits, your commitment to spiritual reflection continues to create space for God to reveal His work and character. The discipline of paying attention to your spiritual journey is itself transformative, developing spiritual sensitivity and awareness that transcends any particular tool or method.",
            "bible_passages": [
                {
                    "reference": "Romans 8:28",
                    "text": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
                    "why_it_fits": "This foundational promise reveals God's ultimate pattern of redemption and transformation—working all circumstances toward good for those aligned with His purposes. It assures us that no experience is wasted in God's economy of grace. Your reflections, even when processed through imperfect means, participate in this transformative pattern as God uses every aspect of your journey for growth and good.",
                    "connection": "The transformative principle is that God specializes in redemption, using all experiences—including limitations and imperfections—to shape us according to His purposes. Our trust in this promise allows us to engage with life reflectively, knowing that even our processing of experiences is part of His good work in us."
                }
            ],
            "practical_steps": [
                "Maintain your practice of spiritual reflection—whether through journaling, meditation, or prayerful consideration of your experiences.",
                "Look for 'God moments' or evidences of His work in your daily life this week, noting them mentally or in writing.",
                "Share one spiritual insight or recognition of God's pattern in your life with someone this week—community reinforces and clarifies spiritual understanding."
            ],
            "prayer_starter": "Lord, teach me to recognize Your good and transformative patterns in my life, even in the midst of limitations and imperfections. Help me to trust Your redeeming work in all circumstances and to see with spiritual eyes how You are shaping me through every experience. Develop in me a reflective heart that notices Your activity and a trusting spirit that rests in Your good purposes.",
            "encouragement": "Your spiritual growth and transformation are not dependent on perfect circumstances or flawless tools. God works through your seeking heart, your reflective practice, and your willingness to pay attention to His work in your life. This very commitment to spiritual awareness is evidence of His transformative work within you, developing maturity and Christ-like character through the consistent practice of reflection and attention to His presence.",
            "pattern_insights": [
                "God works in consistent patterns of faithfulness, redemption, and transformation throughout Scripture and in individual lives—your spiritual journey participates in these eternal patterns.",
                "Your commitment to reflective practice and spiritual awareness is itself part of God's transformative pattern, developing sensitivity to the Holy Spirit and capacity to recognize divine activity in daily life."
            ]
        }

def get_bible_verse_suggestions(themes):
    """
    Get specific Bible verses for identified themes with DEEP EXPLANATIONS of why they fit.
    Returns suggestions with references, themes, and transformative connections.
    """
    # Extract theme names (the part before the dash) for matching
    clean_theme_names = []
    for theme in themes:
        if isinstance(theme, str) and " - " in theme:
            clean_theme_names.append(theme.split(" - ")[0].strip().lower())
        else:
            clean_theme_names.append(str(theme).lower())
    
    # Enhanced verse mapping with DEEP explanations
    theme_to_verses = {
        "new creation": [
            {
                "reference": "2 Corinthians 5:17", 
                "theme": "New Creation",
                "connection": "This verse establishes the transformative reality that in Christ, we become entirely new at our core—not merely improved versions of our old selves. Our identity, nature, and destiny are fundamentally recreated according to God's original design."
            },
            {
                "reference": "Ephesians 4:22-24",
                "theme": "Putting On New Self",
                "connection": "This passage outlines the practical process of living out our new creation identity—consciously putting off old patterns and putting on Christ-like character through renewed thinking and intentional practice."
            }
        ],
        "rest": [
            {
                "reference": "Matthew 11:28-30", 
                "theme": "Rest for the Weary",
                "connection": "Jesus offers rest that is fundamentally relational—coming to Him, learning from Him, taking His yoke. This rest isn't cessation of activity but alignment with His patterns and partnership in His work, which is paradoxically light and freeing."
            },
            {
                "reference": "Hebrews 4:9-11",
                "theme": "Sabbath Rest",
                "connection": "This passage reveals that true Sabbath rest remains available for God's people—a rest that goes beyond physical cessation to spiritual cessation from self-effort and striving, entering God's completed work through faith."
            }
        ],
        "presence": [
            {
                "reference": "Psalm 16:11", 
                "theme": "Fullness of Joy",
                "connection": "God's presence is where we find both the path of life and the fullness of joy. This suggests that true life and genuine joy are found not in circumstances but in conscious, continuous connection with God's presence."
            },
            {
                "reference": "Matthew 28:20",
                "theme": "Constant Presence",
                "connection": "Jesus' promise of constant presence with His followers provides foundational security for the spiritual journey. This awareness transforms how we approach challenges, knowing we never face anything alone."
            }
        ],
        "trust": [
            {
                "reference": "Proverbs 3:5-6", 
                "theme": "Trust and Direction",
                "connection": "This wisdom teaches that wholehearted trust—not relying on our own understanding—is the pathway to divine guidance. The promise isn't that God will make our path easy, but that He will make it straight according to His purposes."
            },
            {
                "reference": "Psalm 37:3-5",
                "theme": "Trust and Delight",
                "connection": "This passage connects trust with active delight in God and commitment of our way to Him. The resulting promise is that God will act on our behalf, bringing His righteousness to light in our situations."
            }
        ],
        "identity": [
            {
                "reference": "Ephesians 2:10", 
                "theme": "God's Masterpiece",
                "connection": "We are God's masterpiece—not merely His creation but His work of art, created for good works that He prepared in advance. This establishes our intrinsic value and purposeful design in Christ."
            },
            {
                "reference": "1 Peter 2:9",
                "theme": "Chosen People",
                "connection": "This verse describes multiple facets of our identity in Christ: chosen, royal, holy, belonging to God. These identities aren't earned but received, transforming how we see ourselves and our purpose."
            }
        ],
        "transformation": [
            {
                "reference": "Romans 12:2", 
                "theme": "Renewed Mind",
                "connection": "Transformation happens through the renewal of our minds—changing how we think to align with God's truth. This mental renewal enables us to discern and live according to God's good, pleasing, and perfect will."
            },
            {
                "reference": "2 Corinthians 3:18",
                "theme": "Beholding Glory",
                "connection": "Our transformation into Christ's image happens as we behold His glory. This suggests that spiritual change is less about effort and more about attention—fixing our gaze on Christ and being changed by what we see."
            }
        ],
        "grace": [
            {
                "reference": "Ephesians 2:8-9", 
                "theme": "Saved by Grace",
                "connection": "Salvation by grace through faith establishes the pattern for the entire Christian life—everything begins with and continues through God's unmerited favor, not our performance or achievement."
            },
            {
                "reference": "2 Corinthians 12:9",
                "theme": "Sufficient Grace",
                "connection": "God's grace is most evident in our weaknesses, not our strengths. His power is perfected in our limitations, transforming what appears to be deficiency into opportunity for divine sufficiency."
            }
        ],
        "peace": [
            {
                "reference": "John 14:27", 
                "theme": "Jesus' Peace",
                "connection": "The peace Jesus gives is fundamentally different from worldly peace—it isn't dependent on circumstances but flows from relationship with Him. This peace guards hearts and minds amid life's turbulence."
            },
            {
                "reference": "Philippians 4:7",
                "theme": "Peace That Guards",
                "connection": "God's peace transcends understanding and actively guards hearts and minds. This suggests that divine peace isn't passive but actively protective, standing watch over our inner lives."
            }
        ],
        "hope": [
            {
                "reference": "Romans 15:13", 
                "theme": "Hope Filled",
                "connection": "God is the source of hope that fills us with joy and peace as we trust Him. This hope isn't wishful thinking but confident expectation based on God's character and promises."
            },
            {
                "reference": "Hebrews 6:19",
                "theme": "Anchor of Hope",
                "connection": "Hope anchors the soul—it provides stability amid life's storms. This anchor is secure because it's fastened behind the heavenly curtain in God's presence, beyond the reach of changing circumstances."
            }
        ],
        "gratitude": [
            {
                "reference": "1 Thessalonians 5:18", 
                "theme": "Thankful in Everything",
                "connection": "Giving thanks in all circumstances is God's will—this practice transforms perspective, helping us recognize God's presence and purposes even in difficult situations."
            },
            {
                "reference": "Colossians 3:15-17",
                "theme": "Thankful Heart",
                "connection": "Thankfulness allows Christ's peace to rule in our hearts and His word to dwell richly within us. Gratitude creates the internal conditions for spiritual wisdom and worshipful living."
            }
        ],
        "reflection": [
            {
                "reference": "Psalm 19:14", 
                "theme": "Reflective Prayer",
                "connection": "This prayer asks that both our words and meditations be pleasing to God, acknowledging that our internal thought life matters to Him and can be offered as worship."
            },
            {
                "reference": "Psalm 77:11-12",
                "theme": "Remembering God's Works",
                "connection": "Reflection on God's past deeds builds faith for present challenges. Remembering His faithfulness provides perspective and hope amid current difficulties."
            }
        ],
        "love": [
            {
                "reference": "1 John 4:7-8", 
                "theme": "Love from God",
                "connection": "Love originates from God, and knowing God enables us to love others. Our capacity to love grows from our connection to Love Himself."
            },
            {
                "reference": "1 Corinthians 13:4-7",
                "theme": "Love's Characteristics",
                "connection": "This description of love provides both a mirror for self-examination and a model for Christ-like relating. Love is active, patient, kind, and enduring—the fullest expression of God's character in human relationships."
            }
        ],
        "faith": [
            {
                "reference": "Hebrews 11:1", 
                "theme": "Faith Defined",
                "connection": "Faith provides assurance about what we hope for and conviction about what we don't see. This spiritual vision enables us to live in light of eternal realities beyond immediate circumstances."
            },
            {
                "reference": "Mark 9:23-24",
                "theme": "Faith and Help",
                "connection": "This interaction shows that honest acknowledgment of faith mixed with doubt is met with Jesus' help. Our 'I believe; help my unbelief' becomes the starting point for His strengthening work."
            }
        ]
    }
    
    suggestions = []
    added_references = set()  # To avoid duplicates
    
    # Find matching verses with DEEP explanations
    for theme_name in clean_theme_names:
        # Check for direct matches
        for key, verses in theme_to_verses.items():
            if key in theme_name or theme_name in key:
                for verse in verses[:2]:  # Get 2 verses per matching theme
                    if verse["reference"] not in added_references:
                        suggestions.append(verse)
                        added_references.add(verse["reference"])
                break  # Found a match, move to next theme
        
        # Also check for partial matches
        if len(suggestions) < 3:  # If we don't have enough suggestions
            for key, verses in theme_to_verses.items():
                # Check if any word in the theme matches
                theme_words = theme_name.split()
                for word in theme_words:
                    if len(word) > 3 and key in word:  # Only check significant words
                        for verse in verses[:1]:
                            if verse["reference"] not in added_references:
                                suggestions.append(verse)
                                added_references.add(verse["reference"])
                        break
    
    # If no suggestions found, provide defaults with DEEP explanations
    if not suggestions:
        suggestions = [
            {
                "reference": "Matthew 6:33", 
                "theme": "Seeking God First",
                "connection": "This foundational teaching establishes the priority principle of the kingdom: seeking God's reign and righteousness above all else. When this vertical alignment is right, horizontal provisions find their proper place. This isn't a formula for material gain but a reorientation of life's center and source."
            },
            {
                "reference": "Philippians 4:6-7", 
                "theme": "Peace Through Prayer",
                "connection": "This passage provides a transformative pattern for dealing with anxiety: moving from worry to prayerful engagement with God. The promise isn't immediate problem resolution but supernatural peace that guards heart and mind amid ongoing circumstances. This peace comes through specific relational practices with God."
            },
            {
                "reference": "Psalm 23:1", 
                "theme": "God as Shepherd",
                "connection": "This beloved psalm portrays God as the attentive, providing, guiding Shepherd. The assurance 'I shall not want' speaks to comprehensive provision—not necessarily everything we desire, but everything we need according to the Shepherd's wisdom and care. This metaphor transforms how we view God's leadership in our lives."
            },
            {
                "reference": "John 3:16", 
                "theme": "God's Love",
                "connection": "This most famous verse reveals the heart of the gospel: God's initiating, sacrificial love for the world. His love motivated the gift of His Son, making eternal life available to all who believe. This love establishes the foundation for our relationship with God—not based on our worthiness but on His character."
            },
            {
                "reference": "Romans 8:28", 
                "theme": "Good from All Things",
                "connection": "This promise assures believers that God works all circumstances—both positive and negative—toward good for those who love Him. This doesn't mean all experiences are good in themselves, but that God can redeem even difficult situations for His purposes and our growth. This transforms how we view life's challenges."
            }
        ]
    
    return suggestions[:5]  # Return up to 5 suggestions