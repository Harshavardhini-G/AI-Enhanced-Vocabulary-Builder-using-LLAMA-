import streamlit as st
import random
from groq import Groq
import pandas as pd

class VocabularyBuilder:
    def __init__(self):
        # Initialize Groq client
        self.client = Groq(api_key='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')
        self.model = "llama-3.3-70b-versatile"
        
        # Predefined word list
        self.word_categories = {
            "Beginner": [
                "happy", "smile", "dream", "learn", "hope", 
                "friend", "light", "peace", "kind", "brave"
            ],
            "Intermediate": [
                "serendipity", "resilience", "eloquent", "empathy", 
                "perspective", "innovative", "challenge", "courage", 
                "harmony", "potential"
            ],
            "Advanced": [
                "ubiquitous", "ephemeral", "quintessential", 
                "melancholy", "enigmatic", "transcendent", 
                "paradigm", "luminous", "arduous", "ethereal"
            ]
        }
    
    def generate_word_details(self, word):
        """Generate comprehensive word details"""
        prompt = f"""
        Provide detailed information for the word "{word}":
        1. Clear definition
        2. Part of speech
        3. Etymology
        4. 3 synonyms
        5. 3 antonyms
        6. 2 example sentences
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating word details: {e}"
    
    def generate_quiz(self, difficulty):
        """Generate a quiz for the given difficulty level"""
        words = self.word_categories.get(difficulty, [])
        quiz_questions = []
        
        for word in random.sample(words, min(5, len(words))):
            prompt = f"""
            Create a multiple-choice question for the word "{word}":
            1. Generate a definition-based multiple-choice question.
            2. Provide 4 options (A, B, C, D) without marking the correct answer in the question text.
            """
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
                
                # Extract question content
                question_content = response.choices[0].message.content
                
                # Fetch the correct answer
                correct_answer_prompt = f"What is the correct answer for the question: {question_content}?"
                correct_answer_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": correct_answer_prompt}],
                    max_tokens=50
                )
                
                quiz_questions.append({
                    'word': word,
                    'question': question_content.strip(),
                    'answer': correct_answer_response.choices[0].message.content.strip()
                })
            
            except Exception as e:
                st.error(f"Error generating quiz for {word}: {e}")
        
        return quiz_questions

def home_page():
    st.title("🚀 AI-Enhanced Vocabulary Builder")
    
    # Create a container with a colored background
    st.markdown("""
    <style>
    .highlight-box {
        background-color: #E6F2FF;  /* Light blue background */
        border: 2px solid #4A90E2;  /* Darker blue border */
        border-radius: 10px;  /* Rounded corners */
        padding: 20px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Use the custom CSS class in a container
    st.markdown("""
    <div class="highlight-box">
        <h2>Welcome to Your Vocabulary Learning Companion!</h2>
        <p>Embark on an exciting journey to expand your vocabulary with our AI-powered learning tool. 
        Whether you're a student, professional, or language enthusiast, we've got you covered.</p>
        <h3>Key Features:</h3>
        <ul>
            <li>Interactive Word Learning</li>
            <li>Personalized Quizzes</li>
            <li>AI-Generated Explanations</li>
            <li>Multiple Difficulty Levels</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.image("https://img.freepik.com/free-vector/dictionary-concept-illustration_114360-3022.jpg", use_container_width=True)

def learn_words_page(vocab_builder):
    st.title("🔍 Vocabulary Learning")
    difficulty = st.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
    words = vocab_builder.word_categories.get(difficulty, [])
    if st.button("Explore Words"):
        for word in words:
            with st.expander(f"🌟 {word.upper()}"):
                details = vocab_builder.generate_word_details(word)
                st.write(details)

def quiz_page(vocab_builder):
    st.title("📝 Vocabulary Quiz")
    
    # Initialize session state variables
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "detailed_results" not in st.session_state:
        st.session_state.detailed_results = []

    difficulty = st.selectbox("Select Quiz Difficulty", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("Start Quiz") or st.session_state.quiz_started:
        if not st.session_state.quiz_started:
            # Reset session state for a new quiz
            st.session_state.quiz_started = True
            st.session_state.quiz_questions = vocab_builder.generate_quiz(difficulty)
            st.session_state.user_answers = {}
            st.session_state.score = 0
            st.session_state.detailed_results = []
        
        quiz_questions = st.session_state.quiz_questions
        total_questions = len(quiz_questions)
        
        # Display quiz questions
        for idx, q in enumerate(quiz_questions, 1):
            st.write(f"### Question {idx}")
            st.write(q['question'])
            user_answer = st.radio("Select your answer:", ["A", "B", "C", "D"], key=f"quiz_{idx}")
            st.session_state.user_answers[idx] = user_answer
        
        if st.button("Submit Quiz"):
            # Evaluate answers using Groq API
            for idx, q in enumerate(quiz_questions, 1):
                # Prepare evaluation prompt
                evaluation_prompt = f"""
                Evaluate the following quiz question:
                Question: {q['question']}
                Correct Answer: {q['answer']}
                User's Selected Answer: {st.session_state.user_answers.get(idx)}

                Please:
                1. Check if the selected answer is correct
                2. Provide a brief explanation
                3. If incorrect, explain why and what the correct answer is
                """
                
                try:
                    # Use Groq API to evaluate the answer
                    evaluation_response = vocab_builder.client.chat.completions.create(
                        model=vocab_builder.model,
                        messages=[{"role": "user", "content": evaluation_prompt}],
                        max_tokens=300
                    )
                    
                    # Get evaluation results
                    evaluation_text = evaluation_response.choices[0].message.content
                    
                    # Determine if the answer is correct
                    is_correct = st.session_state.user_answers.get(idx) == q['answer']
                    if is_correct:
                        st.session_state.score += 1
                    
                    # Store detailed results
                    st.session_state.detailed_results.append({
                        'word': q['word'],
                        'question': q['question'],
                        'user_answer': st.session_state.user_answers.get(idx),
                        'correct_answer': q['answer'],
                        'is_correct': is_correct,
                        'explanation': evaluation_text
                    })
                
                except Exception as e:
                    st.error(f"Error evaluating question {idx}: {e}")
            
            # Display quiz results
            st.success(f"🎉 Quiz Completed! Your Score: {st.session_state.score}/{total_questions}")
            
            # Detailed Results Section
            st.header("Quiz Breakdown")
            for result in st.session_state.detailed_results:
                result_color = "green" if result['is_correct'] else "red"
                st.markdown(f"#### Word: {result['word'].upper()} {'✅' if result['is_correct'] else '❌'}")
                
                with st.expander("Question Details"):
                    st.write(f"**Question:** {result['question']}")
                    st.write(f"**Your Answer:** {result['user_answer']}")
                    st.write(f"**Correct Answer:** {result['correct_answer']}")
                    
                    # Display AI-generated explanation
                    st.markdown(f"**Explanation:** {result['explanation']}")

def faq_page():
    st.title("❓ Frequently Asked Questions")
    
    st.markdown("""
    <style>
    .faq-box {
        background-color: #E6F2FF; /* Light grey background */
        border: 2px solid #e6e6e6; /* Light grey border */
        border-radius: 10px; /* Rounded corners */
        padding: 15px; /* Inner padding for spacing */
        margin: 10px 0; /* Margin between FAQs */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    }
    </style>
    """, unsafe_allow_html=True)

    faqs = [
       {
            "question": "How does the AI help in vocabulary learning?",
            "answer": "Our AI generates personalized word explanations, creates interactive quizzes, and provides context-rich learning experiences."
        },
        {
            "question": "Can I learn words at my own pace?",
            "answer": "Absolutely! We offer multiple difficulty levels from Beginner to Advanced."
        },
        {
            "question": "How often are new words added?",
            "answer": "Our AI continuously updates the word database to provide fresh and relevant vocabulary."
        },
        {
        "question": "How does the AI help in vocabulary learning?",
        "answer": "Our AI generates personalized word explanations, creates interactive quizzes, and provides context-rich learning experiences."
        },
        {
        "question": "Can I learn words at my own pace?",
        "answer": "Absolutely! We offer multiple difficulty levels from Beginner to Advanced."
        },
        {
        "question": "How often are new words added?",
        "answer": "Our AI continuously updates the word database to provide fresh and relevant vocabulary."
        },
        {
        "question": "Does the tool provide examples for word usage?",
        "answer": "Yes, the tool provides context-rich example sentences for every word, helping you understand how to use it in real-world scenarios."
        },
        {
        "question": "Are there any personalized quizzes available?",
        "answer": "Yes, personalized quizzes are generated based on your learning history to reinforce retention and measure progress."
        },
        {
        "question": "Can I track my progress over time?",
        "answer": "Definitely! The tool offers detailed progress tracking with insights into mastered words and areas for improvement."
        },
        {
        "question": "Does the tool support multiple languages?",
        "answer": "Yes, we support vocabulary learning in multiple languages to cater to a global audience."
        }
    ]
    
    for faq in faqs:
        with st.expander(faq['question']):
            st.markdown(f'<div class="faq-box">{faq["answer"]}</div>', unsafe_allow_html=True)

def about_page():

# Title Section
    st.title("🌐 About AI Vocabulary Builder")
    
    # Add CSS for styling
    st.markdown("""
    <style>
    /* Global container styling */
    .section {
        margin: 20px 0;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9; /* Light background */
        border: 2px solid #e6e6e6; /* Light border */
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #2b547e; /* Dark blue for headers */
        font-family: 'Arial', sans-serif;
    }

    /* Bullet points styling */
    ul {
        list-style-type: square;
        padding-left: 20px;
        color: #333333;
    }

    /* Developer cards */
    .developer-card {
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        background-color: #e6f2ff; /* Light blue background */
        border: 2px solid #4a90e2; /* Blue border */
        margin: 10px;
    }
    .developer-card h3 {
        margin-bottom: 5px;
    }
    .developer-card p {
        color: #555555; /* Subtle gray for text */
        font-style: italic;
    }
    .highlight-box {
        background-color: #E6F2FF;  /* Light blue background */
        border: 2px solid #4A90E2;  /* Darker blue border */
        border-radius: 10px;  /* Rounded corners */
        padding: 20px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Mission Section
    st.markdown("""
    <div class="highlight-box">
        <h2>Welcome to Your Vocabulary Learning Companion!</h2>
        <p>Embark on an exciting journey to expand your vocabulary with our AI-powered learning tool. 
        Whether you're a student, professional, or language enthusiast, we've got you covered.</p>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""<div class="highlight-box">
    <H2>Key Features</H2>
    <ul>
        <li>AI-Powered Word Generation</li>
        <li>Adaptive Learning Paths</li>
        <li>Interactive Quizzes</li>
        <li>Multi-Level Difficulty</li>
        <li>Comprehensive Word Insights</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Team Section
    
    st.header("Our Developer")

    developers = [
        {
            "name": "Harshavardhini",
            "role": "AI/ML Lead, UX Designer",
            "description": "Expertise in Natural Language Processing and Machine Learning"
        },
        
    ]

    # Developer cards
    cols = st.columns(len(developers))
    for idx, dev in enumerate(developers):
        with cols[idx]:
            st.markdown(f"""
            <div class="developer-card">
                <h3>{dev['name']}</h3>
                <p><strong>{dev['role']}</strong></p>
                <p>{dev['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Set page configuration FIRST and ONLY ONCE
    st.set_page_config(
        page_title="AI Vocabulary Builder", 
        page_icon="📚", 
        layout="wide"
    )

    # Custom CSS Styling
    st.markdown("""
    <style>
    /* Global Styling */
    body {
        background-color: #f0f4f8;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Container Styling */
    .main-container {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        padding: 20px;
        margin: 10px;
    }

    /* Sidebar Styling */
    .css-1aumxhk {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        color: white;
        border-radius: 10px;
    }

    /* Navigation Button Styling */
    .stRadio > div {
        background-color:#5dade2;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .stRadio > div > label {
        color: white;
        font-weight: bold;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }

    .stRadio > div > label:hover {
        color: #f1c40f;
        transform: scale(1.05);
    }

    /* Header Styling */
    .css-10trblm {
        color: #2c3e50;
        font-weight: bold;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }

    /* Button Styling */
    .stButton > button {
        background-color:#2874a6;
        color: white !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #2980b9 !important;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar styling and navigation
    st.sidebar.markdown("""
    <div style='
        background: linear-gradient(135deg, #2c3e50, #3498db);
        color: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    '>
        <h1 style='
            color: white;
            font-size: 2.5em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        '>VocabAI</h1>
        <p style='
            color: #ecf0f1;
            margin-bottom: 20px;
            font-style: italic;
        '>Your AI Vocabulary Companion</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize VocabularyBuilder
    vocab_builder = VocabularyBuilder()
    
    # Sidebar Navigation
    pages = {
        "Home": home_page,
        "Learn Words": learn_words_page,
        "Quiz": quiz_page,
        "FAQ": faq_page,
        "About": about_page
    }
    
    selection = st.sidebar.radio("**Journey Map**", list(pages.keys()))

    # Page rendering
    if selection == "Learn Words":
        pages[selection](vocab_builder)
    elif selection == "Quiz":
        pages[selection](vocab_builder)
    else:
        pages[selection]()

if __name__ == "__main__":
    main()