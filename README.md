# 🕹️ Game Selection Menu (Python)

**Author:** Alex Murray (@wizrdcodes)  
**Language:** Python (text-based games, modular architecture)

---

## 🎯 Overview
This project is a **multi-game Python application** featuring a main selection menu that allows players to choose from a variety of minigames — including guessing, logic, and a story-driven RPG.  

The structure is designed to demonstrate clean organization, reusable functions, and modular imports — making it a great example of both **game logic design** and **software architecture**.

---

## 🧩 Included Games

### 🎲 Variety of Minigames
- **Guessing Game** – A number-guessing challenge that gives players feedback after each attempt.  
- **Rock Paper Scissors** – A simple interactive classic with random computer choices.  
- **Infinity Game** – A looping, ever-escalating challenge built for experimentation with control flow.

These games show a fun variety of beginner-to-intermediate Python logic, input handling, and user interaction.

---

### ⚔️ Role-Playing Death Game (RPG)
A modular text-based adventure featuring branching paths, item management, and persistent game states.  
This component demonstrates more **complex backend design**, including:
- Multi-file architecture (`dark_forest.py`, `helper_functions.py`, etc.)
- Centralized `game_state` and `player_state` tracking  
- Scene-based story progression and replay handling  
- Randomized events and conditional branching  

The RPG is fully runnable and **actively being expanded** with new scenes, logic layers, and features.

---

## 🧠 Technical Highlights
- Modularized imports for each game  
- State tracking with dictionaries (`game_state`, `player_state`)  
- Clear function-based scene logic  
- Organized directory structure for easy navigation  
- Compatibility with Python 3.13+  

---

## 🧰 How to Run
From the project root:

```bash
python Game_Selection.py
```

Then follow the on-screen instructions to choose which game to play.

You can quit any time by entering:
```
q
```

---

## 📂 Project Structure
- `Game_Selection.py` – Main menu and entry point  
- `games_package/` – Contains each game module  
  - `Role_Playing_Death_Game/` – The RPG adventure  
  - `dark_forest.py`, `helper_functions.py`, etc. – Core RPG logic  
- `utils/` – Helper functions and shared utilities  
- `.gitignore`, `requirements.txt` – Environment and project setup files  

---

## 💡 Future Plans
- Add new areas, enemies, and endings to the RPG  
- Improve scene navigation and save/load features  
- Add a simple GUI wrapper for the menu in future versions  
- Continue refining code modularity and testing coverage  

---

## 🧩 License
This repository is shared publicly for educational and portfolio purposes.
