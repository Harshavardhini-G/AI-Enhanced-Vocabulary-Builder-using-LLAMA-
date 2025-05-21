# 🚀 AI-Enhanced Vocabulary Builder

An intelligent vocabulary learning application powered by LLaMA 3 and Groq API. Designed to help learners at **Beginner**, **Intermediate**, and **Advanced** levels master new words through AI-generated explanations and quizzes.

![Vocabulary Banner](https://img.freepik.com/free-vector/dictionary-concept-illustration_114360-3022.jpg)

---

## 🔍 Features

* 🎓 **Level-Based Word Lists** (Beginner, Intermediate, Advanced)
* 🤖 **AI-Generated Word Details**: Definitions, synonyms, antonyms, etymology, and examples
* 🧠 **Dynamic Quizzes**: AI-generated multiple-choice questions and answers
* 🎨 **Interactive UI**: Built using Streamlit with modern layout

---

## 📦 Tech Stack

| Technology    | Description                             |
| ------------- | --------------------------------------- |
| **Python**    | Backend logic and API handling          |
| **Streamlit** | UI and Web app deployment               |
| **Groq API**  | Chat-based LLaMA 3.1-70B for generation |
| **Pandas**    | Data handling (for future extensions)   |

---

## 🛠️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/vocabulary-builder.git
   cd vocabulary-builder
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   ```bash
   streamlit run vocabulary-builder.py
   ```

---

## 🔑 Configuration

This app uses the [Groq API](https://console.groq.com/) to access LLaMA 3 models. Replace the API key in `VocabularyBuilder.__init__` with your own:

```python
self.client = Groq(api_key='your-api-key')
```

---

## 🚧 Future Enhancements

* User login and progress tracking
* Flashcard mode
* Downloadable word lists
* Text-to-speech support

---

## 🤝 Contributing

Contributions, ideas, and feedback are welcome! Feel free to fork this repo and submit pull requests.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

 
