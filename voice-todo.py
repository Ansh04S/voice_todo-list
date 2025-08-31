import json
import os
import re
import time
from dataclasses import dataclass, asdict
from typing import List

import pyttsx3

def speak(text: str):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

USE_VOICE = True
try:
    import speech_recognition as sr
    r = sr.Recognizer()
    VOICE_OK = True
except Exception:
    VOICE_OK = False

DATA_FILE = "tasks.json"

@dataclass
class Task:
    id: int
    text: str
    done: bool = False
    created_at: float = time.time()

class ToDo:
    def __init__(self, path=DATA_FILE):
        self.path = path
        self.tasks: List[Task] = []
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                self.tasks = [tasks(**t) for t in raw]
            except Exception:
                self.tasks = []
        else:
            self.tasks = []
        self._reassign_ids()

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self.tasks], f, ensure_ascii=False, indent=2)
    
    def _reassign_ids(self):
        for i, t in enumerate(self.tasks, start=1):
            t.id = i

    def add (self, text: str):
        self.tasks.append(Task(id=len(self.tasks)+1, text=text.strip()))
        self._save()
        return self.tasks[-1]
    
    def list(self):
        return self.tasks
    
    def mark_done(self, idx: int):
        if 1 <= idx <= len(self.tasks):
            self.tasks[idx-1].done = True
            self._save()
            return True
        return False
    
    def remove(self, idx: int):
        if 1 <= idx <= len(self.tasks):
            removed = self.tasks.pop(idx-1)
            self._reassign_ids()
            self._save()
            return removed
        return None
    
    def clear(self):
        self.tasks = []
        self._save()

HELP_TEXT = (
    "Say or type commands like:\n"
    " . add buy milk\n"
    " . list\n"
    " . done 2\n"
    " . remove 3\n"
    " . clear\n"
    " . help\n"
    " . exit\n"
    "Tip: You can also say sentences, e.g., 'add a task to call mom' or 'mark task 2 done'."
)

CMD_PATTERNS = [
    ("add",    re.compile(r"^(?:add|create|remember|note)\s+(.*)$", re.I)),
    ("list",   re.compile(r"^(?:list|show|display)(?:\s+tasks?)?$", re.I)),
    ("done",   re.compile(r"^(?:done|complete|finish|mark\s+done)\s+(\d+)$", re.I)),
    ("remove", re.compile(r"^(?:remove|delete)\s+(\d+)$", re.I)),
    ("clear",  re.compile(r"^(?:clear|reset)(?:\s+all)?$", re.I)),
    ("help",   re.compile(r"^(?:help|\?)$", re.I)),
    ("exit",   re.compile(r"^(?:exit|quit|close|bye)$", re.I)),
]

def parse_command(text: str):
    t = text.strip()
    m = re.match(r"^(?:add|create).*(?:to\s+)?(.+)$", t, re.I)
    if m and not any(t.lower().startswith(x) for x in ["list", "done", "remove", "clear", "help", "exit"]):
        return("add", m.group(1))
    

    m = re.search(r"(?:task\s+)?(\d+)\s+(?:is\s+)?(?:done|complete|finished)", t, re.I)
    if m:
        return ("done", m.group(1))

    m = re.search(r"(?:delete|remove)\s+(?:task\s+)?(\d+)", t, re.I)
    if m:
        return ("remove", m.group(1))
    
    for name, pat in CMD_PATTERNS:
        m = pat.match(t)
        if m:
            return (name, m.group(1) if m.lastindex else None)
        
    if len(t.split()) >= 2:
        return ("add", t)

    return (None, None)

def hear_once(timeout=5, phrase_time_limit=7):
    if not VOICE_OK:
        return None
    with sr.Microphone() as source:
        print("Listening... (say something)")
        r.adjust_for_ambient_noise(source, dureation=0.5)
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except Exception:
        return None

def prompt_input():
    if VOICE_OK and USE_VOICE:
        text = hear_once()
        if text is None:
            print("Mic unavailable-switching to text mode.")
            speak("Microphone unavailable. Switching to text mode.")
            return input("Type command: ").strip()
        elif text == "":
            print("Didn't catch that. Try again or type instead.")
            return input("Type command: ").strip()
        else:
            print(f"You said: {text}")
            return text.strip()
    else:
        return input("Type command: ").strip()

def show_tasks(tasks: List[Task]):
    if not tasks:
        print("No tasks yet.")
        return 
    print("\nYour Tasks:")
    for t in tasks:
        status = "✓" if t.done else "."   
        print(f" {t.id}. {status} {t.text}")
    print("")

def main():
    todo = ToDo()
    print("=== Voice To-Do List ===")
    print("Speak or type your command. Say 'help' for options.")
    if VOICE_OK:
        print("Voice input is ON. (Will fall back to text if recognition fails.)")
    else:
        print("Voice packages not available-using text mode.")

    speak("Voice to do list is ready. Say a command.")

    while True:
        user = prompt_input()
        if not user:
            continue

        cmd, arg = parse_command(user)

        if cmd == "help":
            print(HELP_TEXT)
            speak("Here are some examples you can say or type.")
        elif cmd == "list":
            show_tasks(todo.list())
            speak(f"You have {len(todo.list())} tasks.")
        elif cmd == "add" and arg:
            task = todo.add(arg)
            print(f"Added: {task.text}")
            speak(f"Added task: {task.text}")
        elif cmd == "done" and arg:
            try:
                idx = int(arg)
                ok = todo.mark_done(idx)
                if ok:
                    print(f"Marked task {idx} done.")
                    speak(f"Marked task {idx} done.")
                else:
                    print("Invalid task number.")
                    speak("Invalid task number.")
            except ValueError:
                print("Please specify a valid task number, e.g., 'done 2'.") 
        elif cmd == "remove" and arg:
            try:
                idx = int(arg)
                removed = todo.remove(idx)
                if removed:
                    print(f"Removed: {removed.text}")
                    speak(f"Removed task {idx}.")
                else:
                    print("Invalid task number.")
                    speak("Invalid task number.")
            except ValueError:
                print("Please specify a valid task number, e.g., 'remove 3'.")
        elif cmd == "clear":
            todo.clear()
            print("All tasks cleared.")
            speak("All tasks cleared.")
        elif cmd == "exit":
            print("Goodbye!")
            speak("Goodbye.")
            break
        else:
            print("Didn't understand. Type 'help' for examples.")
            speak("I did not understand. Say help for examples.")

if __name__ == "__main__":
    main()
