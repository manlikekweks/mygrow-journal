# ============================================
# IMPORT ALL MODULES AT THE TOP
# ============================================

# Import Streamlit FIRST
import streamlit as st

# Import all other standard modules
import json
import datetime
import os
import sys
from collections import Counter
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random

# ============================================
# GOOGLE AUTHENTICATION CHECK - UPDATED API
# ============================================

# Check if user is authenticated
try:
    # New Streamlit authentication API
    from streamlit.runtime.state import get_session_state
    
    # Get authentication state
    auth_state = get_session_state().get("_auth", {})
    is_authenticated = auth_state.get("is_authenticated", False)
    user_info = auth_state.get("user_info", {})
    
    if not is_authenticated:
        st.markdown("""
            <div style="text-align: center; padding: 4rem;">
                <h1 style="color: #2D5A27;">🔐 MyGrow AI Spiritual Director</h1>
                <p style="color: #5A7F5C; font-size: 1.2rem; margin-bottom: 2rem;">
                    Sign in to access your personal spiritual journal.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Login button
        if st.button("Sign in with Google", type="primary", use_container_width=True, icon="🔑"):
            st.switch_page("/oauth2/authorize")
        st.stop()
    
    # User is logged in
    user_id = user_info.get("sub", "unknown")
    user_email = user_info.get("email", "")
    user_name = user_info.get("name", user_email)
    
except Exception as e:
    # Fallback for development
    st.warning(f"Authentication error: {e}")
    user_id = "dev_user"
    user_email = "dev@example.com"
    user_name = "Developer"

# Optional: Show welcome message in sidebar later
# st.sidebar.success(f"Welcome, {user_email}!")

# ============================================
# IMPORT AI MODULES WITH PROPER ERROR HANDLING
# ============================================

# Now try to import your AI modules
try:
    from ai_analyzer import analyze_spiritual_journal, get_bible_verse_suggestions
    from bible_integration import get_bible_verse, get_book_list, get_chapter_list, get_verse_list
    ai_ready = True
    bible_ready = True
    
except ImportError as e:
    # Don't use st.error here - it might not be initialized yet
    print(f"⚠️ Module import error: {e}")
    
    # Set flags
    ai_ready = False
    bible_ready = False
    
    # Define fallback functions that don't use Streamlit
    def analyze_spiritual_journal(journal_text):
        return {
            "error": "AI module not loaded",
            "primary_themes": ["Faith", "Hope"],
            "emotional_state": ["Reflective"],
            "core_question": "How can I connect with God today?",
            "key_insight": "Your openness is the first step toward deeper understanding.",
            "bible_passages": [
                {
                    "reference": "Matthew 6:33",
                    "text": "But seek first the kingdom of God and his righteousness, and all these things will be added to you.",
                    "why_it_fits": "Encourages prioritizing spiritual growth"
                }
            ],
            "practical_steps": [
                "Spend 10 minutes in quiet reflection",
                "Write down one thing you're grateful for",
                "Reach out to someone in need"
            ],
            "prayer_starter": "Lord, guide my heart as I seek You today.",
            "encouragement": "Every step forward matters."
        }
    
    def get_bible_verse_suggestions(themes):
        return [{"reference": "John 3:16", "theme": "Love"}]
    
    def get_bible_verse(reference, version="WEB"):
        return "Bible module not loaded"
    
    def get_book_list():
        return ["Genesis", "Psalms", "Matthew", "John"]
    
    def get_chapter_list(book):
        return list(range(1, 11))
    
    def get_verse_list(book, chapter):
        return list(range(1, 11))

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="MyGrow AI Spiritual Director",
    page_icon="🌿", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# TRANQUIL HEADER
# ============================================
st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
        <h1 style="color: #2D5A27; margin-bottom: 0.5rem;">🌿 MyGrow AI Spiritual Director</h1>
        <p style="color: #5A7F5C; font-size: 1.1rem;">📚 Journal • 📖 Scripture • 📈 Growth Tracking • 💝 Personalized Guidance</p>
        <hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 1.5rem 0; border: none;">
    </div>
""", unsafe_allow_html=True)

# ============================================
# ENHANCED JOURNAL ARCHIVE CLASS WITH MONTH FILTERING
# ============================================

class JournalArchive:
    def __init__(self, user_id):  # MODIFIED: Accept user_id parameter
        # MODIFIED: Create user-specific data directory
        self.user_id = user_id
        self.data_dir = f"user_data/{user_id}"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # MODIFIED: All file paths are now inside the user's folder
        self.entries_file = os.path.join(self.data_dir, "journal_entries.json")
        self.patterns_file = os.path.join(self.data_dir, "user_patterns.json")
        self.timeline_file = os.path.join(self.data_dir, "growth_timeline.json")
        
        # Initialize files if they don't exist
        self._init_files()
    
    def _init_files(self):
        """Initialize empty data files."""
        defaults = {
            self.entries_file: [],
            self.patterns_file: {},
            self.timeline_file: []
        }
        
        for file, default in defaults.items():
            if not os.path.exists(file):
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump(default, f, ensure_ascii=False, indent=2)
    
    def save_entry(self, journal_text, analysis_result):
        """Save a complete journal entry with analysis."""
        entry_id = str(datetime.datetime.now().timestamp())
        
        entry = {
            "id": entry_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "journal_text": journal_text,
            "analysis": analysis_result,
            "themes": analysis_result.get("primary_themes", []),
            "emotions": analysis_result.get("emotional_state", []),
            "bible_passages": analysis_result.get("bible_passages", []),
            "practical_steps": analysis_result.get("practical_steps", []),
            "word_count": len(journal_text.split())
        }
        
        # Load existing entries
        try:
            with open(self.entries_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
        except:
            entries = []
        
        # Add new entry
        entries.append(entry)
        
        # Save back
        with open(self.entries_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        
        # Update patterns and timeline
        self._update_patterns(entries)
        self._update_timeline(entry)
        
        return entry
    
    def _update_patterns(self, entries):
        """Analyze patterns across all entries."""
        if not entries:
            return
        
        # Collect data
        all_themes = []
        all_emotions = []
        all_verses = []
        
        for entry in entries:
            all_themes.extend(entry.get("themes", []))
            all_emotions.extend(entry.get("emotions", []))
            for passage in entry.get("bible_passages", []):
                all_verses.append(passage.get("reference", ""))
        
        # Calculate frequencies
        theme_counter = Counter(all_themes)
        emotion_counter = Counter(all_emotions)
        verse_counter = Counter(all_verses)
        
        # Writing patterns
        word_counts = [e.get("word_count", 0) for e in entries]
        avg_word_count = sum(word_counts) / len(word_counts) if word_counts else 0
        
        # Build patterns object
        patterns = {
            "last_updated": datetime.datetime.now().isoformat(),
            "total_entries": len(entries),
            "theme_patterns": {
                "most_common": dict(theme_counter.most_common(10)),  # Changed from 5 to 10
                "all_frequencies": dict(theme_counter)
            },
            "emotion_patterns": {
                "most_common": dict(emotion_counter.most_common(5)),
                "trends": self._detect_emotion_trends(entries)
            },
            "bible_patterns": {
                "most_referenced": dict(verse_counter.most_common(5)),
                "favorite_books": self._analyze_bible_books(all_verses)
            },
            "writing_patterns": {
                "average_length": avg_word_count,
                "frequency_days": self._calculate_frequency(entries)
            },
            "growth_indicators": self._calculate_growth_indicators(entries)
        }
        
        # Save patterns
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, ensure_ascii=False, indent=2)
    
    def _detect_emotion_trends(self, entries):
        """Detect emotion trends over time."""
        if len(entries) < 2:
            return {}
        
        # Group by week
        weekly_emotions = {}
        for entry in entries:
            date = datetime.datetime.fromisoformat(entry["timestamp"])
            week_key = f"{date.year}-W{date.isocalendar()[1]:02d}"
            
            if week_key not in weekly_emotions:
                weekly_emotions[week_key] = []
            
            weekly_emotions[week_key].extend(entry.get("emotions", []))
        
        # Calculate most common per week
        trends = {}
        for week, emotions in weekly_emotions.items():
            if emotions:
                counter = Counter(emotions)
                trends[week] = counter.most_common(2)
        
        return trends
    
    def _analyze_bible_books(self, verses):
        """Analyze which Bible books are most referenced."""
        books = []
        for verse in verses:
            if " " in verse:
                book = verse.split(" ")[0]
                books.append(book)
        
        return dict(Counter(books).most_common(5)) if books else {}
    
    def _calculate_frequency(self, entries):
        """Calculate journaling frequency."""
        if len(entries) < 2:
            return "Just starting"
        
        dates = sorted([e["date"] for e in entries])
        first_date = datetime.datetime.strptime(dates[0], "%Y-%m-%d")
        last_date = datetime.datetime.strptime(dates[-1], "%Y-%m-%d")
        days_diff = (last_date - first_date).days + 1
        
        freq = len(entries) / days_diff
        
        if freq >= 0.7:
            return "Daily writer"
        elif freq >= 0.3:
            return "Regular writer"
        elif freq >= 0.14:
            return "Weekly writer"
        else:
            return "Occasional writer"
    
    def _calculate_growth_indicators(self, entries):
        """Calculate growth indicators."""
        if len(entries) < 3:
            return {"stage": "Beginning", "indicators": []}
        
        recent = entries[-3:]  # Last 3 entries
        older = entries[:3]    # First 3 entries
        
        # Compare themes
        recent_themes = set()
        older_themes = set()
        
        for entry in recent:
            recent_themes.update(entry.get("themes", []))
        for entry in older:
            older_themes.update(entry.get("themes", []))
        
        indicators = []
        
        if len(recent_themes) > len(older_themes):
            indicators.append("Exploring more spiritual themes")
        
        # Check for action steps
        action_words = ["completed", "done", "finished", "accomplished", "achieved"]
        recent_text = " ".join([e["journal_text"].lower() for e in recent])
        if any(word in recent_text for word in action_words):
            indicators.append("Taking practical steps forward")
        
        # Check for gratitude
        gratitude_words = ["thank", "grateful", "appreciate", "blessed", "thankful"]
        recent_gratitude = sum(1 for word in gratitude_words if word in recent_text)
        older_text = " ".join([e["journal_text"].lower() for e in older])
        older_gratitude = sum(1 for word in gratitude_words if word in older_text)
        
        if recent_gratitude > older_gratitude:
            indicators.append("Growing in gratitude")
        
        return {
            "stage": "Growing" if indicators else "Developing",
            "indicators": indicators,
            "theme_diversity_increase": len(recent_themes) - len(older_themes)
        }
    
    def _update_timeline(self, new_entry):
        """Update growth timeline with milestone detection."""
        with open(self.timeline_file, 'r', encoding='utf-8') as f:
            timeline = json.load(f)
        
        # Detect milestones
        milestones = self._detect_milestones(new_entry, timeline)
        
        for milestone in milestones:
            timeline.append({
                "timestamp": new_entry["timestamp"],
                "type": milestone["type"],
                "description": milestone["description"],
                "entry_id": new_entry["id"]
            })
        
        # Keep only last 20 milestones
        if len(timeline) > 20:
            timeline = timeline[-20:]
        
        with open(self.timeline_file, 'w', encoding='utf-8') as f:
            json.dump(timeline, f, ensure_ascii=False, indent=2)
    
    def _detect_milestones(self, entry, existing_timeline):
        """Detect growth milestones in new entry."""
        milestones = []
        existing_types = [m["type"] for m in existing_timeline]
        
        # Longest entry
        if entry.get("word_count", 0) > 300 and "long_reflection" not in existing_types:
            milestones.append({
                "type": "long_reflection",
                "description": f"Deep reflection ({entry['word_count']} words)"
            })
        
        # New theme
        entry_themes = set(entry.get("themes", []))
        if entry_themes and "new_theme" not in existing_types:
            milestones.append({
                "type": "new_theme",
                "description": f"Exploring new theme: {list(entry_themes)[0]}"
            })
        
        # Bible engagement
        bible_passages = entry.get("bible_passages", [])
        if len(bible_passages) >= 2 and "scripture_engagement" not in existing_types:
            milestones.append({
                "type": "scripture_engagement",
                "description": "Engaging deeply with Scripture"
            })
        
        # 5th entry milestone
        entries = self.get_entries()
        if len(entries) == 5 and "five_entries" not in existing_types:
            milestones.append({
                "type": "five_entries",
                "description": "Completed 5 journal entries - building a habit!"
            })
        
        return milestones
    
    def get_entries(self, limit=None):
        """Get journal entries, optionally limited."""
        try:
            with open(self.entries_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            
            if limit:
                return entries[-limit:]
            return entries
        except:
            return []
    
    # ============================================
    # NEW: MONTH FILTERING METHODS - ADDED TO FIX JANUARY 2026 ISSUE
    # ============================================
    
    def get_entries_by_year_month(self, year_month: str):
        """Get entries for a specific month (format: '2026-01')."""
        entries = self.get_entries()
        filtered = []
        
        for entry in entries:
            entry_date = entry.get("date", "")
            
            # Parse date - assuming format "YYYY-MM-DD"
            try:
                if "-" in entry_date:
                    parts = entry_date.split("-")
                    if len(parts) >= 2:
                        entry_year_month = f"{parts[0]}-{parts[1]}"
                        if entry_year_month == year_month:
                            filtered.append(entry)
            except (ValueError, IndexError):
                continue
        
        return filtered
    
    def get_all_months_with_entries(self):
        """Get list of all months with entries (YYYY-MM format)."""
        entries = self.get_entries()
        months_set = set()
        
        for entry in entries:
            entry_date = entry.get("date", "")
            if "-" in entry_date:
                parts = entry_date.split("-")
                if len(parts) >= 2:
                    months_set.add(f"{parts[0]}-{parts[1]}")
        
        # Sort descending (most recent first)
        return sorted(list(months_set), reverse=True)
    
    def get_monthly_summary(self, year_month: str):
        """Get detailed summary for a specific month."""
        entries = self.get_entries_by_year_month(year_month)
        
        if not entries:
            return {
                "month": year_month,
                "entry_count": 0,
                "top_themes": {},
                "top_emotions": {},
                "average_words": 0,
                "unique_scriptures": 0
            }
        
        # Collect data
        all_themes = []
        all_emotions = []
        word_counts = []
        bible_verses = []
        
        for entry in entries:
            all_themes.extend(entry.get("themes", []))
            all_emotions.extend(entry.get("emotions", []))
            word_counts.append(entry.get("word_count", 0))
            for passage in entry.get("bible_passages", []):
                bible_verses.append(passage.get("reference", ""))
        
        # Calculate stats
        theme_counter = Counter(all_themes)
        emotion_counter = Counter(all_emotions)
        
        return {
            "month": year_month,
            "entry_count": len(entries),
            "top_themes": dict(theme_counter.most_common(5)),  # Show top 5 themes per month
            "top_emotions": dict(emotion_counter.most_common(3)),
            "average_words": sum(word_counts) // len(word_counts) if word_counts else 0,
            "unique_scriptures": len(set(bible_verses)),
            "first_entry_date": entries[0].get("date"),
            "last_entry_date": entries[-1].get("date")
        }
    
    def get_monthly_summaries(self):
        """Get summaries for all months with entries."""
        months = self.get_all_months_with_entries()
        summaries = []
        
        for month in months:
            summary = self.get_monthly_summary(month)
            summaries.append(summary)
        
        return summaries
    
    def get_patterns(self):
        """Get analyzed patterns."""
        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def get_timeline(self):
        """Get growth timeline."""
        try:
            with open(self.timeline_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def get_summary_insights(self):
        """Generate summary insights for the user."""
        patterns = self.get_patterns()
        entries = self.get_entries()
        
        if not entries:
            return {
                "total_entries": 0,
                "insights": ["Welcome to your spiritual journey!"],
                "next_suggestion": "Write your first reflection to begin tracking your growth."
            }
        
        # Build insights
        insights = []
        
        # Theme insights
        common_themes = patterns.get("theme_patterns", {}).get("most_common", {})
        if common_themes:
            themes_list = list(common_themes.items())
            if themes_list:
                top_theme, top_count = themes_list[0]
                insights.append(f"Your spiritual heart centers on **{top_theme}** (appeared {top_count} times)")
                
                # Add secondary theme insight if available
                if len(themes_list) > 1:
                    second_theme, second_count = themes_list[1]
                    insights.append(f"Secondary focus: **{second_theme}** ({second_count} occurrences)")
        
        # Growth indicators
        growth = patterns.get("growth_indicators", {})
        if growth.get("indicators"):
            insights.extend([f"✓ {ind}" for ind in growth["indicators"]])
        
        # Writing pattern
        writing = patterns.get("writing_patterns", {})
        insights.append(f"Writing rhythm: **{writing.get('frequency_days', 'developing')}**")
        
        # Bible engagement
        bible = patterns.get("bible_patterns", {})
        top_book = list(bible.get("favorite_books", {}).keys())[0] if bible.get("favorite_books") else None
        if top_book:
            insights.append(f"Most engaged Scripture: **{top_book}**")
        
        return {
            "total_entries": len(entries),
            "insights": insights[:4],  # Show up to 4 insights
            "next_suggestion": self._get_next_suggestion(patterns)
        }
    
    def _get_next_suggestion(self, patterns):
        """Get personalized suggestion for growth."""
        total = patterns.get("total_entries", 0)
        
        if total < 3:
            return "Try exploring different spiritual themes in your next reflection."
        elif total < 10:
            common_themes = patterns.get("theme_patterns", {}).get("most_common", {})
            if common_themes and len(common_themes) >= 2:
                themes = list(common_themes.keys())
                return f"Consider how **{themes[0]}** and **{themes[1]}** connect in your spiritual journey."
            return "Reflect on how your understanding has evolved since you started journaling."
        else:
            common_themes = patterns.get("theme_patterns", {}).get("most_common", {})
            if common_themes:
                theme = list(common_themes.keys())[0]
                return f"Your deep focus on **{theme}** shows spiritual maturity. What new aspect of this theme could you explore?"
        
        return "Your consistent journaling reveals a beautiful spiritual journey. Keep listening to your heart."

# ============================================
# ENHANCED GROWTH DASHBOARD WITH 10-THEME PIE CHART
# ============================================

def create_growth_dashboard(archive):
    """Create an enhanced growth dashboard with detailed theme analysis."""
    
    entries = archive.get_entries()
    
    if not entries:
        st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <h1 style="color: #2D5A27;">📊 Your Growth Journey</h1>
                <p style="color: #5A7F5C;">Start journaling to see insights appear here</p>
            </div>
            <div style="background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                <h3 style="color: #2D5A27; margin: 0 0 1rem 0;">🌱 Begin Your Journey</h3>
                <p style="color: #5A7F5C; font-size: 1.1rem;">
                    Your spiritual growth dashboard will appear here once you start journaling. 
                    Each reflection adds color to your journey.
                </p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # ===== TRANQUIL DASHBOARD HEADER =====
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
            <h1 style="color: #2D5A27; margin-bottom: 0.5rem;">📊 Your Spiritual Growth Dashboard</h1>
            <p style="color: #5A7F5C; font-size: 1.1rem;">Track your journey in a tranquil space</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ===== KEY METRICS WITH TRANQUIL CARDS =====
    patterns = archive.get_patterns()
    
    st.markdown('<div style="display: flex; gap: 1rem; margin: 2rem 0;">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style='background: white; border: 1px solid #E8E6DE; border-radius: 8px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <div style='font-size: 2.5rem; font-weight: bold; color: #2D5A27; margin: 0.5rem 0;'>{len(entries)}</div>
                <div style='font-size: 0.9rem; color: #5A7F5C; text-transform: uppercase; letter-spacing: 0.5px;'>Total Entries</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if len(entries) > 1:
            first_date = datetime.datetime.fromisoformat(entries[0]["timestamp"]).date()
            last_date = datetime.datetime.fromisoformat(entries[-1]["timestamp"]).date()
            days = (last_date - first_date).days + 1
            st.markdown(f"""
                <div style='background: white; border: 1px solid #E8E6DE; border-radius: 8px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <div style='font-size: 2.5rem; font-weight: bold; color: #2D5A27; margin: 0.5rem 0;'>{days}</div>
                    <div style='font-size: 0.9rem; color: #5A7F5C; text-transform: uppercase; letter-spacing: 0.5px;'>Journey Days</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background: white; border: 1px solid #E8E6DE; border-radius: 8px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <div style='font-size: 2.5rem; font-weight: bold; color: #2D5A27; margin: 0.5rem 0;'>1</div>
                    <div style='font-size: 0.9rem; color: #5A7F5C; text-transform: uppercase; letter-spacing: 0.5px;'>First Step</div>
                </div>
            """, unsafe_allow_html=True)
    
    with col3:
        writing = patterns.get("writing_patterns", {})
        freq = writing.get("frequency_days", "Beginning")
        st.markdown(f"""
            <div style='background: white; border: 1px solid #E8E6DE; border-radius: 8px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <div style='font-size: 1.8rem; font-weight: bold; color: #2D5A27; margin: 0.5rem 0;'>{freq}</div>
                <div style='font-size: 0.9rem; color: #5A7F5C; text-transform: uppercase; letter-spacing: 0.5px;'>Writing Style</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        growth = patterns.get("growth_indicators", {})
        stage = growth.get("stage", "Beginning")
        st.markdown(f"""
            <div style='background: white; border: 1px solid #E8E6DE; border-radius: 8px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <div style='font-size: 1.8rem; font-weight: bold; color: #2D5A27; margin: 0.5rem 0;'>{stage}</div>
                <div style='font-size: 0.9rem; color: #5A7F5C; text-transform: uppercase; letter-spacing: 0.5px;'>Growth Stage</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 2.5rem 0; border: none;">', unsafe_allow_html=True)
    
    # ===== FIXED: MONTHLY SUMMARY SECTION =====
    st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 8px; border: 1px solid #E8E6DE; margin-bottom: 2rem;'>
            <h2 style='color: #2D5A27; margin-top: 0;'>📅 Monthly Insights</h2>
            <p style='color: #5A7F5C; margin-bottom: 1.5rem;'>
                Your reflection journey over time
            </p>
    """, unsafe_allow_html=True)
    
    # Get all monthly summaries using the new method
    monthly_summaries = archive.get_monthly_summaries()
    
    # Debug info (optional - can remove after testing)
    with st.expander("🔍 Debug: See all months", expanded=False):
        st.write(f"Total entries: {len(entries)}")
        all_months = archive.get_all_months_with_entries()
        st.write(f"Months found: {all_months}")
        
        # Check specifically for January 2026
        if "2026-01" in all_months:
            st.success("✅ January 2026 found in months list!")
            jan_entries = archive.get_entries_by_year_month("2026-01")
            st.write(f"January 2026 entries: {len(jan_entries)}")
            for entry in jan_entries[:3]:
                st.write(f"  - {entry.get('date')}: {entry.get('journal_text', '')[:50]}...")
        else:
            st.warning("❌ January 2026 NOT found in months list")
        
        st.write(f"Monthly summaries: {len(monthly_summaries)}")
    
    if not monthly_summaries:
        st.info("No monthly data available yet")
    else:
        # Display monthly summaries
        for summary in monthly_summaries:
            month_name = datetime.datetime.strptime(summary["month"] + "-01", "%Y-%m-%d").strftime("%B %Y")
            
            with st.expander(f"**{month_name}** ({summary['entry_count']} entries)", 
                           expanded=(summary == monthly_summaries[0])):
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.markdown(f"""
                        <div style='background: white; border: 1px solid #E8E6DE; border-radius: 8px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                            <div style='font-size: 2.5rem; font-weight: bold; color: #2D5A27; margin: 0.5rem 0;'>{summary['average_words']}</div>
                            <div style='font-size: 0.9rem; color: #5A7F5C; text-transform: uppercase; letter-spacing: 0.5px;'>Avg. Words</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    theme_count = len(summary.get('top_themes', {}))
                    st.markdown(f"""
                        <div style='background: white; border: 1px solid #E8E6DE; border-radius: 8px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                            <div style='font-size: 2.5rem; font-weight: bold; color: #2D5A27; margin: 0.5rem 0;'>{theme_count}</div>
                            <div style='font-size: 0.9rem; color: #5A7F5C; text-transform: uppercase; letter-spacing: 0.5px;'>Key Themes</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_c:
                    st.markdown(f"""
                        <div style='background: white; border: 1px solid #E8E6DE; border-radius: 8px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                            <div style='font-size: 2.5rem; font-weight: bold; color: #2D5A27; margin: 0.5rem 0;'>{summary.get('unique_scriptures', 0)}</div>
                            <div style='font-size: 0.9rem; color: #5A7F5C; text-transform: uppercase; letter-spacing: 0.5px;'>Scriptures</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Top themes for the month
                top_themes = summary.get('top_themes', {})
                if top_themes:
                    st.markdown("**Most Common Themes:**")
                    theme_display = ""
                    for theme, count in top_themes.items():
                        theme_display += f'<span style="background-color: #2D5A27; color: white; padding: 4px 10px; margin: 2px; border-radius: 15px; font-size: 13px; display: inline-block;">{theme} ({count})</span> '
                    
                    st.markdown(theme_display, unsafe_allow_html=True)
                
                # Check if this is January 2026
                if summary["month"] == "2026-01":
                    st.success(f"✅ Found {summary['entry_count']} entries for January 2026!")
                    st.balloons()  # Celebrate!
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 2.5rem 0; border: none;">', unsafe_allow_html=True)
    
    # ===== ENHANCED SHAPE OF MY HEART PIE CHART (10 THEMES) =====
    st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 8px; border: 1px solid #E8E6DE; margin-bottom: 2rem;'>
            <h2 style='color: #2D5A27; margin-top: 0;'>💝 Shape of My Heart</h2>
            <p style='color: #5A7F5C; margin-bottom: 1.5rem;'>
                Your spiritual focus revealed through all your reflections
            </p>
    """, unsafe_allow_html=True)
    
    # Collect ALL themes from ALL entries
    all_themes = []
    for entry in entries:
        all_themes.extend(entry.get("themes", []))
    
    if all_themes:
        theme_counts = Counter(all_themes)
        total_themes = len(all_themes)
        
        # Get top 10 themes (instead of 3)
        top_themes = theme_counts.most_common(10)
        
        # Calculate "Other" category for remaining themes
        top_theme_names = [theme for theme, count in top_themes]
        top_theme_counts = [count for theme, count in top_themes]
        
        other_count = sum(count for theme, count in theme_counts.items() if theme not in top_theme_names)
        
        # Prepare data for pie chart
        labels = top_theme_names
        values = top_theme_counts
        
        if other_count > 0:
            labels.append("Other Themes")
            values.append(other_count)
        
        # Enhanced color palette for 10+ themes
        colors = [
            '#2D5A27', '#3A7344', '#5A7F5C', '#6B9A7A', 
            '#8AB4A1', '#9CC4B0', '#A3C4D9', '#8BB8D9',
            '#6DA3C9', '#4E8EB9', '#C1D4E6', '#E8F4F8'
        ]
        
        # Create enhanced donut chart
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker_colors=colors[:len(labels)],
            textinfo='label+percent',
            insidetextorientation='radial',
            hoverinfo='label+value+percent',
            textfont=dict(size=12, family="Georgia"),
            marker=dict(line=dict(color='white', width=1)),
            pull=[0.05 if i < 3 else 0 for i in range(len(labels))]  # Slight pull for top 3
        )])
        
        fig.update_layout(
            height=450,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
                font=dict(size=11, family="Georgia"),
                itemwidth=40
            ),
            margin=dict(t=40, b=120, l=40, r=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(
                text="Distribution of Your Spiritual Focus",
                font=dict(size=16, family="Georgia", color='#2D5A27'),
                x=0.5,
                y=0.95
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ===== ENHANCED AI ANALYSIS FOR "SHAPE OF MY HEART" =====
        
        if top_themes:
            primary_theme, primary_count = top_themes[0]
            secondary_theme = top_themes[1][0] if len(top_themes) > 1 else None
            tertiary_theme = top_themes[2][0] if len(top_themes) > 2 else None
            
            primary_percentage = (primary_count / total_themes) * 100
            
            # Generate AI-powered insights
            insights = []
            
            # Primary theme insight
            if primary_percentage > 30:
                insights.append(f"**{primary_theme}** is your dominant spiritual focus ({primary_percentage:.0f}%), showing deep commitment to this area.")
            elif primary_percentage > 15:
                insights.append(f"**{primary_theme}** is your primary spiritual focus ({primary_percentage:.0f}%), indicating consistent reflection on this theme.")
            else:
                insights.append(f"**{primary_theme}** emerges as your main focus ({primary_percentage:.0f}%), revealing what matters most to your heart.")
            
            # Diversity insight
            unique_themes = len(theme_counts)
            if unique_themes >= 8:
                insights.append(f"Your heart explores **{unique_themes} different themes**, showing beautiful spiritual diversity.")
            elif unique_themes >= 4:
                insights.append(f"You engage with **{unique_themes} spiritual themes**, demonstrating well-rounded spiritual growth.")
            
            # Secondary themes insight
            if secondary_theme and tertiary_theme:
                insights.append(f"Supported by **{secondary_theme}** and **{tertiary_theme}**, creating a balanced spiritual landscape.")
            
            # Spiritual journey insight
            if total_themes > 20:
                insights.append(f"With **{total_themes} theme occurrences** across your journey, your spiritual life is rich and multifaceted.")
            
            # Display enhanced insights
            st.markdown('<div style="background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">', unsafe_allow_html=True)
            st.markdown("### ✨ What Your Heart Reveals")
            st.markdown('<p style="color: #5A7F5C; font-size: 1.1rem; margin-bottom: 1rem;">Your spiritual focus patterns:</p>', unsafe_allow_html=True)
            
            for insight in insights:
                st.markdown(insight)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Theme combinations insight
            if secondary_theme and tertiary_theme:
                st.markdown('<div style="background: #F0F7ED; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #5A7F5C; margin-top: 1rem;">', unsafe_allow_html=True)
                st.markdown("### 💭 Spiritual Synergy")
                st.markdown(f"Your top three themes—**{primary_theme}**, **{secondary_theme}**, and **{tertiary_theme}**—work together to shape your spiritual understanding. Consider how they might connect in your journey.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('<div style="background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">', unsafe_allow_html=True)
        st.markdown("### ✨ Awaiting Your Reflections")
        st.markdown("As you journal more, this chart will reveal the beautiful shape of your spiritual heart. Each reflection adds color to your unique spiritual journey.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 2.5rem 0; border: none;">', unsafe_allow_html=True)
    
    # ===== ENHANCED PERSONAL INSIGHTS =====
    st.markdown('<div style="background: white; padding: 2rem; border-radius: 8px; border: 1px solid #E8E6DE; margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.markdown("## 💡 Personal Insights")
    st.markdown('<p style="color: #5A7F5C; margin-bottom: 1.5rem;">Wisdom distilled from your spiritual journey</p>', unsafe_allow_html=True)
    
    insights = archive.get_summary_insights()
    for insight in insights.get("insights", []):
        st.markdown('<div style="background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">', unsafe_allow_html=True)
        st.markdown(insight)  # This will process the **bold** text
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Next step suggestion
    st.markdown('<div style="background: white; border-left: 4px solid #2D5A27; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">', unsafe_allow_html=True)
    st.markdown("### 🌱 Next Step on Your Journey")
    st.markdown(insights.get('next_suggestion', 'Keep journaling!'))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== MILESTONES =====
    timeline = archive.get_timeline()
    if timeline:
        st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 2.5rem 0; border: none;">', unsafe_allow_html=True)
        
        st.markdown('<div style="background: white; padding: 2rem; border-radius: 8px; border: 1px solid #E8E6DE;">', unsafe_allow_html=True)
        st.markdown("## ⭐ Milestones")
        st.markdown('<p style="color: #5A7F5C; margin-bottom: 1.5rem;">Celebrating your journey</p>', unsafe_allow_html=True)
        
        for milestone in reversed(timeline[-10:]):
            date = datetime.datetime.fromisoformat(milestone["timestamp"]).strftime("%b %d, %Y")
            
            emoji_map = {
                "long_reflection": "📝",
                "new_theme": "🎨",
                "scripture_engagement": "📖",
                "five_entries": "🎯",
                "ten_entries": "🏆"
            }
            
            emoji = emoji_map.get(milestone["type"], "⭐")
            
            st.markdown(f"""
                <div style='display: flex; align-items: center; gap: 1rem; padding: 1rem; margin: 0.5rem 0; background: #F9F7F1; border-radius: 6px;'>
                    <div style='font-size: 1.5rem;'>{emoji}</div>
                    <div style='flex: 1;'>
                        <div style='font-weight: 500; color: #2D5A27;'>{milestone['description']}</div>
                        <div style='font-size: 0.85rem; color: #5A7F5C; font-family: "Courier New", monospace;'>{date}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export option
    st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 2.5rem 0; border: none;">', unsafe_allow_html=True)
    
    if st.button("📥 Export My Growth Report", use_container_width=True):
        _export_growth_report(archive)

def _export_growth_report(archive):
    """Export growth report as JSON."""
    import json
    
    report = {
        "export_date": datetime.datetime.now().isoformat(),
        "summary": archive.get_summary_insights(),
        "patterns": archive.get_patterns(),
        "timeline": archive.get_timeline(),
        "recent_entries": archive.get_entries(5)
    }
    
    filename = f"mygrow_growth_report_{datetime.datetime.now().strftime('%Y%m%d')}.json"
    
    st.download_button(
        label="📥 Download Full Report (JSON)",
        data=json.dumps(report, indent=2),
        file_name=filename,
        mime="application/json"
    )

# ============================================
# INITIALIZE SESSION STATE & ARCHIVE
# ============================================

# Initialize session state
if 'result' not in st.session_state:
    st.session_state.result = None
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False
if 'show_archive' not in st.session_state:
    st.session_state.show_archive = False
if 'selected_entry' not in st.session_state:
    st.session_state.selected_entry = None

# MODIFIED: Initialize archive with user_id
archive = JournalArchive(user_id)

# ============================================
# SIDEBAR WITH TRANQUIL DESIGN + LOGOUT BUTTON
# ============================================

with st.sidebar:
    # Welcome message
    st.sidebar.success(f"Welcome, {user_name}!")
    
    st.markdown("""
        <div style='background: #F9F7F1; padding: 1.5rem; border-radius: 8px; border: 1px solid #E8E6DE; margin-bottom: 1rem;'>
            <h3 style='color: #2D5A27; margin-top: 0;'>🧭 Navigation</h3>
    """, unsafe_allow_html=True)
    
    # Status indicator
    if ai_ready:
        st.success("✅ AI & Bible: READY")
    else:
        st.error("❌ Setup incomplete (using mock data)")
    
    # Quick stats
    entries = archive.get_entries()
    if entries:
        patterns = archive.get_patterns()
        st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 1rem 0; border: none;">', unsafe_allow_html=True)
        st.markdown("### 📊 Quick Stats")
        st.markdown(f"""
            <div style='background: white; border: 1px solid #E8E6DE; border-radius: 8px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <div style='font-size: 2.5rem; font-weight: bold; color: #2D5A27; margin: 0.5rem 0;'>{len(entries)}</div>
                <div style='font-size: 0.9rem; color: #5A7F5C; text-transform: uppercase; letter-spacing: 0.5px;'>Total Entries</div>
            </div>
        """, unsafe_allow_html=True)
        
        if patterns.get("theme_patterns", {}).get("most_common"):
            theme_counts = patterns["theme_patterns"]["most_common"]
            top_themes = list(theme_counts.items())[:3]
            theme_text = ", ".join([f"{theme}" for theme, count in top_themes])
            st.caption(f"Top themes: **{theme_text}**")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Journal Tools
    st.markdown("""
        <div style='background: #F9F7F1; padding: 1.5rem; border-radius: 8px; border: 1px solid #E8E6DE; margin: 1rem 0;'>
            <h3 style='color: #2D5A27; margin-top: 0;'>📚 Journal Tools</h3>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    if st.button("🏠 Main Journal", use_container_width=True, icon="🏠"):
        st.session_state.show_dashboard = False
        st.session_state.show_archive = False
        st.rerun()
    
    if st.button("📈 Growth Dashboard", use_container_width=True, icon="📈"):
        st.session_state.show_dashboard = True
        st.session_state.show_archive = False
        st.rerun()
    
    if st.button("📖 View Archive", use_container_width=True, icon="📖"):
        st.session_state.show_archive = True
        st.session_state.show_dashboard = False
        st.rerun()
    
    # Auto-archive toggle
    st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 1rem 0; border: none;">', unsafe_allow_html=True)
    auto_archive = st.checkbox("💾 Auto-archive entries", value=True, 
                              help="Automatically save each analysis session")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ADDED: Logout button
    st.markdown("""
        <div style='background: #F0F7ED; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #5A7F5C; margin-top: 1rem;'>
            <h4 style='color: #2D5A27; margin-top: 0;'>👤 Account</h4>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Sign Out", use_container_width=True):
        st.switch_page("/oauth2/logout")  # Updated logout method
    
    st.markdown("""
        </div>
    """, unsafe_allow_html=True)
    
    # Journal tips
    st.markdown("""
        <div style='background: #F0F7ED; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #5A7F5C; margin-top: 1rem;'>
            <h4 style='color: #2D5A27; margin-top: 0;'>📝 Journal Tips</h4>
            <ul style='margin: 0; padding-left: 1.2rem; color: #5A7F5C; font-size: 0.9rem;'>
                <li>Be honest about struggles</li>
                <li>Note Scripture that speaks to you</li>
                <li>Identify what you're seeking</li>
                <li>Review past entries for patterns</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT - DASHBOARD VIEW
# ============================================

if st.session_state.show_dashboard:
    create_growth_dashboard(archive)
    st.stop()

# ============================================
# MAIN CONTENT - ARCHIVE VIEW WITH FIXED SORTING
# ============================================

if st.session_state.show_archive:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
            <h1 style="color: #2D5A27; margin-bottom: 0.5rem;">📚 Journal Archive</h1>
            <p style="color: #5A7F5C; font-size: 1.1rem;">Your past reflections and insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    entries = archive.get_entries()
    
    if not entries:
        st.markdown("""
            <div style="background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                <h3 style="color: #2D5A27; margin: 0 0 1rem 0;">📖 Archive Empty</h3>
                <p style="color: #5A7F5C; font-size: 1.1rem;">
                    No archived entries yet. Save a session to begin.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("← Back to Journal", use_container_width=True):
            st.session_state.show_archive = False
            st.rerun()
        st.stop()
    
    # Archive controls
    st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #E8E6DE; margin-bottom: 2rem;'>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search entries", placeholder="Search by theme, emotion, or keyword")
    with col2:
        sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First"])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Filter entries
    filtered_entries = entries
    if search_term:
        search_lower = search_term.lower()
        filtered_entries = [
            e for e in entries 
            if (search_lower in e.get("journal_text", "").lower() or
                any(search_lower in theme.lower() for theme in e.get("themes", [])) or
                any(search_lower in emotion.lower() for emotion in e.get("emotions", [])))
        ]
    
    # FIXED: Proper sorting by date (not just reverse)
    if sort_order == "Newest First":
        # Sort by timestamp descending (newest first)
        filtered_entries.sort(
            key=lambda x: datetime.datetime.fromisoformat(x["timestamp"].replace('Z', '+00:00')), 
            reverse=True
        )
    else:  # Oldest First
        # Sort by timestamp ascending (oldest first)
        filtered_entries.sort(
            key=lambda x: datetime.datetime.fromisoformat(x["timestamp"].replace('Z', '+00:00')), 
            reverse=False
        )
    
    # Display entries
    for i, entry in enumerate(filtered_entries[-50:]):  # Show more entries (50)
        date = datetime.datetime.fromisoformat(entry["timestamp"]).strftime("%b %d, %Y")
        
        # Debug: Show date for January 2026 entries
        show_debug = False
        if "2026-01" in entry.get("date", ""):
            show_debug = True
        
        with st.expander(f"📅 {date} - {', '.join(entry.get('themes', ['Reflection'])[:2])}", expanded=False):
            
            if show_debug:
                st.success(f"✅ January 2026 entry found! (Date: {entry.get('date')})")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Themes:** {', '.join(entry.get('themes', []))}")
                st.markdown(f"**Emotions:** {', '.join(entry.get('emotions', []))}")
            with col_b:
                st.markdown(f"**Length:** {entry.get('word_count', 0)} words")
                st.markdown(f"**Bible Passages:** {len(entry.get('bible_passages', []))}")
            
            st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 1.5rem 0; border: none;">', unsafe_allow_html=True)
            st.markdown("**Journal Preview:**")
            st.markdown(entry.get("journal_text", "")[:200] + "..." if len(entry.get("journal_text", "")) > 200 else entry.get("journal_text", ""))
            
            if st.button(f"🔍 View Full Analysis", key=f"view_archive_{i}_{entry.get('id', i)}"):
                st.session_state.selected_entry = entry
                st.session_state.show_archive = False
                st.rerun()
    
    # Show sorting debug info
    with st.expander("🔍 Sorting Debug Info", expanded=False):
        st.write(f"Total entries: {len(entries)}")
        st.write(f"Filtered entries: {len(filtered_entries)}")
        st.write(f"Sort order: {sort_order}")
        
        # Show dates of first 5 entries
        st.write("First 5 entries in current order:")
        for i, entry in enumerate(filtered_entries[:5]):
            st.write(f"  {i+1}. {entry.get('date')} - {entry.get('timestamp')}")
        
        # Check for January 2026 entries
        jan_2026 = [e for e in filtered_entries if "2026-01" in e.get("date", "")]
        st.write(f"January 2026 entries in filtered list: {len(jan_2026)}")
        if jan_2026:
            st.success("✅ January 2026 entries found!")
            for e in jan_2026:
                st.write(f"  - {e.get('date')}: {e.get('journal_text', '')[:50]}...")
    
    # Archive stats
    st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 1.5rem 0; border: none;">', unsafe_allow_html=True)
    st.markdown("### 📊 Archive Statistics")
    
    if entries:
        all_themes = [theme for entry in entries for theme in entry.get('themes', [])]
        if all_themes:
            theme_counts = pd.Series(all_themes).value_counts()
            st.bar_chart(theme_counts.head(10))  # Show top 10 in bar chart
    
    if st.button("← Back to Journal", use_container_width=True):
        st.session_state.show_archive = False
        st.rerun()
    
    st.stop()

# ============================================
# MAIN CONTENT - JOURNAL VIEW (DEFAULT)
# ============================================

# Two column layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div style='background-color: #F9F7F1; padding: 2rem; border-radius: 2px; border: 1px solid #E8E6DE; margin: 1rem 0;'>
            <h2 style='margin: 0 0 1rem 0; color: #2D5A27;'>📝 Your Reflection</h2>
    """, unsafe_allow_html=True)
    
    # Journal input
    journal = st.text_area(
        "Paste your journal or AI conversation:",
        height=250,
        placeholder="Example: Today I felt anxious about work...\nWhat I'm seeking: peace and guidance...\n\n(Write 50+ characters for meaningful guidance)",
        value="",
        key="journal_input"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analysis button
    if st.button("🌄 Seek Spiritual Guidance", type="primary", use_container_width=True):
        if journal and len(journal.strip()) > 50:
            with st.spinner("Seeking wisdom from Scripture through AI..."):
                result = analyze_spiritual_journal(journal)
                st.session_state.result = result
                
                # Auto-archive if enabled
                if 'auto_archive' in locals() and auto_archive:
                    try:
                        archive.save_entry(journal, result)
                    except Exception as e:
                        st.sidebar.warning(f"Could not archive: {str(e)[:50]}")
        else:
            st.warning("Please write more for meaningful guidance (50+ characters minimum)")
    
    # Display results if available
    if st.session_state.result:
        result = st.session_state.result
        
        if "error" in result:
            st.error(f"Analysis error: {result['error']}")
        else:
            # Display RICH results in tranquil cards
            st.markdown("""
                <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
                    <h2 style="color: #2D5A27; margin-bottom: 0.5rem;">📖 Spiritual Guidance</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # ===== COMPACT THEMES & EMOTIONS DISPLAY =====
            themes = result.get("primary_themes", [])[:4]  # Limit to 4
            emotions = result.get("emotional_state", [])[:3]  # Limit to 3
            
            # FIX APPLIED HERE: Use f-string to fix the ({len(emotions)}) issue
            themes_count = len(themes)
            emotions_count = len(emotions)
            
            # Compact two-column display
            st.markdown(f"""
                <div style="display: flex; gap: 1.5rem; margin: 1.5rem 0; padding: 0;">
                    <!-- Themes Column -->
                    <div style="flex: 1; background: #F9F7F1; border: 1px solid #E8E6DE; border-radius: 6px; padding: 0.8rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; font-size: 0.9rem; font-weight: 600; color: #2D5A27;">
                            <span style="font-size: 1rem;">✨</span>
                            <span>Spiritual Themes</span>
                            <span style="font-size: 0.75rem; color: #8AB4A1; margin-left: 0.25rem; font-weight: normal;">({themes_count})</span>
                        </div>
                        <div style="margin: 0; padding: 0;">
            """, unsafe_allow_html=True)
            
            # Display themes as compact badges
            for theme in themes:
                st.markdown(f'<span style="display: inline-block; background: #2D5A27; color: white; padding: 0.25rem 0.6rem; margin: 0.2rem 0.3rem 0.2rem 0; border-radius: 12px; font-size: 0.8rem; font-weight: 500; white-space: nowrap;">{theme}</span>', unsafe_allow_html=True)
            
            st.markdown(f"""
                        </div>
                    </div>
                    
                    <!-- Emotions Column -->
                    <div style="flex: 1; background: #F9F7F1; border: 1px solid #E8E6DE; border-radius: 6px; padding: 0.8rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; font-size: 0.9rem; font-weight: 600; color: #2D5A27;">
                            <span style="font-size: 1rem;">💖</span>
                            <span>Heart State</span>
                            <span style="font-size: 0.75rem; color: #8AB4A1; margin-left: 0.25rem; font-weight: normal;">({emotions_count})</span>
                        </div>
                        <div style="margin: 0; padding: 0;">
            """, unsafe_allow_html=True)
            
            # Display emotions as compact badges
            for emotion in emotions:
                st.markdown(f'<span style="display: inline-block; background: #5A7F5C; color: white; padding: 0.25rem 0.6rem; margin: 0.2rem 0.3rem 0.2rem 0; border-radius: 12px; font-size: 0.8rem; font-weight: 500; white-space: nowrap;">{emotion}</span>', unsafe_allow_html=True)
            
            st.markdown("""
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Core Question (immediately after compact section)
            question = result.get("core_question", "")
            if question:
                st.markdown(f"""
                    <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                        <h3 style='color: #2D5A27; margin: 0 0 1rem 0;'>💭 The Heart of Your Reflection</h3>
                        <p style='font-size: 1.1rem; color: #5A7F5C; font-style: italic;'>{question}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Key Insight
            insight = result.get("key_insight", "")
            if insight:
                st.markdown(f"""
                    <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                        <h3 style='color: #2D5A27; margin: 0 0 1rem 0;'>💡 Key Insight</h3>
                        <p style='font-size: 1.1rem;'>{insight}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Bible Passages - FIXED FONT ISSUE
            passages = result.get("bible_passages", [])
            if passages:
                st.markdown(f"""
                    <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                        <h3 style='color: #2D5A27; margin: 0 0 1rem 0;'>📖 Scripture for You</h3>
                """, unsafe_allow_html=True)
                
                for passage in passages[:3]:
                    st.markdown(f"""
                        <div style='margin-bottom: 1.5rem; padding-left: 1rem; border-left: 3px solid #8AB4A1;'>
                            <div style='font-weight: 600; color: #2D5A27; font-size: 1.1rem;'>{passage.get('reference', 'Bible Verse')}</div>
                            <div style='font-style: italic; color: #5A7F5C; margin: 0.75rem 0; font-size: 1.05rem; line-height: 1.5;'>"{passage.get('text', '')}"</div>
                            <div style='font-size: 0.95rem; color: #5A7F5C; line-height: 1.5; margin-top: 0.5rem;'>
                                <span style='font-weight: 600; color: #2D5A27;'>Why this fits:</span> {passage.get('why_it_fits', '')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Practical Steps
            steps = result.get("practical_steps", [])
            if steps:
                steps_html = ""
                for i, step in enumerate(steps, 1):
                    steps_html += f"<li style='margin-bottom: 0.5rem;'>{step}</li>"
                
                st.markdown(f"""
                    <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                        <h3 style='color: #2D5A27; margin: 0 0 1rem 0;'>✨ Practical Steps</h3>
                        <ul style='margin:0; padding-left: 1.5rem; font-size: 1.1rem;'>{steps_html}</ul>
                    </div>
                """, unsafe_allow_html=True)
            
            # Prayer
            prayer = result.get("prayer_starter", "")
            if prayer:
                st.markdown(f"""
                    <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                        <h3 style='color: #2D5A27; margin: 0 0 1rem 0;'>🙏 Prayer Starter</h3>
                        <p style='font-size: 1.1rem; font-style: italic; color: #5A7F5C;'>{prayer}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Encouragement
            encouragement = result.get("encouragement", "")
            if encouragement:
                st.markdown(f"""
                    <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                        <h3 style='color: #2D5A27; margin: 0 0 1rem 0;'>💝 Encouragement</h3>
                        <p style='font-size: 1.1rem; color: #2D5A27;'>{encouragement}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Archive button
            if not auto_archive:
                if st.button("💾 Save to Archive", type="secondary", use_container_width=True):
                    archive.save_entry(journal, result)
                    st.success("Entry archived!")

with col2:
    st.markdown("""
        <div style='background: #F9F7F1; padding: 1.5rem; border-radius: 8px; border: 1px solid #E8E6DE; margin-bottom: 1rem;'>
            <h3 style='color: #2D5A27; margin-top: 0;'>🔍 Quick Bible Lookup</h3>
    """, unsafe_allow_html=True)
    
    if ai_ready and st.session_state.result and 'primary_themes' in st.session_state.result:
        # Show verse suggestions based on current analysis
        st.markdown("**📚 Suggested Verses**")
        suggestions = get_bible_verse_suggestions(st.session_state.result['primary_themes'])
        for suggestion in suggestions[:3]:
            if st.button(f"{suggestion.get('reference', 'Bible Verse')}", 
                       key=f"btn_{suggestion.get('reference', '')}",
                       use_container_width=True):
                verse_text = get_bible_verse(suggestion.get('reference', 'John 3:16'), "WEB")
                st.markdown(f"""
                    <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                        <div style='font-weight: 500; color: #2D5A27;'>{suggestion.get('reference', 'Bible Verse')}</div>
                        <div style='font-style: italic; color: #5A7F5C; margin-top: 0.5rem;'>{verse_text[:200] + "..." if len(verse_text) > 200 else verse_text}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    # Manual lookup
    st.markdown("**🔎 Look Up Any Verse**")
    manual_verse = st.text_input("Reference:", "Matthew 6:33", key="manual_verse")
    if st.button("Get This Verse", use_container_width=True):
        text = get_bible_verse(manual_verse, "WEB")
        if text.startswith("❌"):
            st.error(text)
        else:
            st.markdown(f"""
                <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                    <div style='font-weight: 500; color: #2D5A27;'>{manual_verse}</div>
                    <div style='font-style: italic; color: #5A7F5C; margin-top: 0.5rem;'>{text}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ENTRY DETAIL VIEW (if selected from archive)
# ============================================

if st.session_state.selected_entry:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
            <h1 style="color: #2D5A27; margin-bottom: 0.5rem;">📄 Archived Entry Details</h1>
            <p style="color: #5A7F5C; font-size: 1.1rem;">Your past reflection and insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    entry = st.session_state.selected_entry
    date = datetime.datetime.fromisoformat(entry["timestamp"]).strftime("%B %d, %Y at %I:%M %p")
    
    st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #E8E6DE; margin-bottom: 1rem;'>
            <h3 style='color: #2D5A27; margin-top: 0;'>📅 {date}</h3>
            <div style='display: flex; gap: 2rem; margin-top: 1rem;'>
                <div>
                    <div style='font-size: 0.9rem; color: #5A7F5C;'>Themes</div>
                    <div style='font-weight: 500;'>{', '.join(entry.get('themes', []))}</div>
                </div>
                <div>
                    <div style='font-size: 0.9rem; color: #5A7F5C;'>Emotions</div>
                    <div style='font-weight: 500;'>{', '.join(entry.get('emotions', []))}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Original journal
    st.markdown("""
        <div style='background-color: #F9F7F1; padding: 2rem; border-radius: 2px; border: 1px solid #E8E6DE; margin: 1rem 0;'>
            <h4 style='color: #2D5A27; margin-top: 0;'>📝 Original Journal Entry</h4>
    """, unsafe_allow_html=True)
    st.write(entry.get("journal_text", ""))
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analysis results
    analysis = entry.get("analysis", {})
    
    if analysis.get("core_question"):
        st.markdown(f"""
            <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                <h4 style='color: #2D5A27; margin: 0 0 0.5rem 0;'>💭 Core Question</h4>
                <p style='font-size: 1.1rem; color: #5A7F5C; font-style: italic;'>{analysis["core_question"]}</p>
            </div>
        """, unsafe_allow_html=True)
    
    if analysis.get("key_insight"):
        st.markdown(f"""
            <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                <h4 style='color: #2D5A27; margin: 0 0 0.5rem 0;'>💡 Key Insight</h4>
                <p style='font-size: 1.1rem;'>{analysis["key_insight"]}</p>
            </div>
        """, unsafe_allow_html=True)
    
    if analysis.get("bible_passages"):
        st.markdown(f"""
            <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                <h4 style='color: #2D5A27; margin: 0 0 0.5rem 0;'>📖 Bible Passages</h4>
        """, unsafe_allow_html=True)
        for passage in analysis["bible_passages"]:
            st.markdown(f"""
                <div style='margin-bottom: 1rem; padding-left: 1rem; border-left: 3px solid #8AB4A1;'>
                    <div style='font-weight: 600; color: #2D5A27; font-size: 1.1rem;'>{passage.get('reference', 'Verse')}</div>
                    <div style='font-style: italic; color: #5A7F5C; margin: 0.75rem 0; font-size: 1.05rem; line-height: 1.5;'>"{passage.get('text', '')}"</div>
                    <div style='font-size: 0.95rem; color: #5A7F5C; line-height: 1.5; margin-top: 0.5rem;'>
                        <span style='font-weight: 600; color: #2D5A27;'>Why this fits:</span> {passage.get('why_it_fits', '')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if analysis.get("practical_steps"):
        steps_html = ""
        for i, step in enumerate(analysis["practical_steps"], 1):
            steps_html += f"<li style='margin-bottom: 0.5rem;'>{step}</li>"
        
        st.markdown(f"""
            <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                <h4 style='color: #2D5A27; margin: 0 0 0.5rem 0;'>✨ Practical Steps</h4>
                <ul style='margin:0; padding-left: 1.5rem; font-size: 1.1rem;'>{steps_html}</ul>
            </div>
        """, unsafe_allow_html=True)
    
    if analysis.get("prayer_starter"):
        st.markdown(f"""
            <div style='background: white; border-left: 4px solid #8AB4A1; padding: 1.5rem; margin: 1rem 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
                <h4 style='color: #2D5A27; margin: 0 0 0.5rem 0;'>🙏 Prayer</h4>
                <p style='font-size: 1.1rem; font-style: italic; color: #5A7F5C;'>{analysis["prayer_starter"]}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 2.5rem 0; border: none;">', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Archive", use_container_width=True):
            st.session_state.selected_entry = None
            st.session_state.show_archive = True
            st.rerun()
    with col2:
        if st.button("🏠 Back to Journal", use_container_width=True):
            st.session_state.selected_entry = None
            st.rerun()

# ============================================
# FOOTER
# ============================================

st.markdown('<hr style="height: 1px; background: linear-gradient(90deg, transparent, #8AB4A1, transparent); margin: 2.5rem 0; border: none;">', unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #5A7F5C; border-top: 1px solid #E8E6DE;'>
        <p style='font-size: 0.9rem;'>
            🌿 MyGrow AI Spiritual Director v2.0 • 📚 Automatic Archiving • 📈 Growth Tracking • 💝 Personalized Guidance
        </p>
    </div>
""", unsafe_allow_html=True)