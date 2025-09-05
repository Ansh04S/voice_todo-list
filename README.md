# voice_todo-list

# 📝 Voice To-Do List

A smart **voice-enabled To-Do List application** built with **Python** that allows users to add, manage, and track tasks using **speech commands**. The app provides both **voice interaction** and a **beautiful dashboard interface** for seamless productivity.

---

## 🚀 Features

- 🎙️ **Voice Input Support** – Add tasks using your voice.  
- 📋 **Task Management** – Add, mark complete, delete, and view tasks.  
- 🖥️ **Dashboard UI** – Interactive and user-friendly interface.  
- 🔊 **Voice Feedback** – System reads out your tasks for confirmation.  
- 💾 **Persistent Storage** – Saves tasks locally for later use.  
- 🌐 **Scalable Design** – Can be extended for online sync and reminders.  

---

## 🛠️ Tech Stack

- **Frontend (UI)** – Tkinter / Flask / Streamlit (choose based on implementation)  
- **Speech Recognition** – [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)  
- **Text-to-Speech** – [pyttsx3](https://pypi.org/project/pyttsx3/)  
- **Database/Storage** – SQLite / JSON / CSV  
- **Programming Language** – Python 3.x  

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/voice-to-do-list.git
cd voice-to-do-list
````

Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the application:

```bash
python app.py
```

🎤 Speak commands like:

* **"Add task Buy groceries"**
* **"Show my tasks"**
* **"Mark task one as complete"**
* **"Delete task two"**

---

## 📸 Screenshots

### Dashboard View

![Dashboard Screenshot](docs/dashboard.png)

### Voice Interaction

![Voice Command Screenshot](docs/voice.png)

---

## 📂 Project Structure

```
voice-to-do-list/
│── app.py                # Main application file
│── requirements.txt       # Python dependencies
│── tasks.db / tasks.json  # Local storage for tasks
│── static/                # CSS, JS, images (if Flask/Streamlit)
│── templates/             # HTML templates (if Flask)
│── docs/                  # Documentation assets (screenshots)
└── README.md              # Project documentation
```

---

## ✅ Roadmap

* [x] Basic task CRUD with voice commands
* [x] Dashboard UI
* [ ] Reminders with notifications
* [ ] Cloud sync with Google Tasks/Trello
* [ ] Mobile version

---

## 🤝 Contributing

Contributions are welcome!
Feel free to open an **Issue** or submit a **Pull Request**.

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Developed by **[Your Name](https://github.com/your-username)** 🚀

```

---

Do you want me to also create a **`requirements.txt` file** (with SpeechRecognition, pyttsx3, etc.) so you can directly upload both `README.md` and dependencies to GitHub?
```
