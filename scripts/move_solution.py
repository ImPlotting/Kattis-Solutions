import json
import shutil
from pathlib import Path

# Set the root directory to the current directory where the script is located
ROOT_DIR = Path(__file__).resolve().parent.parent

# Define the path to the directories for C and C++ solutions
C_DIR = ROOT_DIR / 'Kattis' / 'C'
CPP_DIR = ROOT_DIR / 'Kattis' / 'C++'
NEW_PROBS_DIR = ROOT_DIR / 'new_probs'
README_FILE = ROOT_DIR / 'README.md'

# Ensure the language directories are correct
assert C_DIR.exists(), f"Directory {C_DIR} does not exist"
assert CPP_DIR.exists(), f"Directory {CPP_DIR} does not exist"

def move_new_problems():
    for difficulty in ['1_Easy', '2_Medium', '3_Hard']:
        for lang_dir in [C_DIR, CPP_DIR]:
            prob_dir = lang_dir / difficulty
            prob_dir.mkdir(parents=True, exist_ok=True)

    for problem in NEW_PROBS_DIR.iterdir():
        if problem.is_dir():
            difficulty = problem.name.split('_')[0]
            for lang_dir in problem.iterdir():
                if lang_dir.is_dir() and lang_dir.name in ['C', 'C++']:
                    target_dir = C_DIR if lang_dir.name == 'C' else CPP_DIR
                    target_dir = target_dir / difficulty
                    shutil.move(str(lang_dir), str(target_dir))
                    info = {
                        'name': problem.name,
                        'difficulty': difficulty,
                        'language': lang_dir.name
                    }
                    with open(target_dir / lang_dir.name / 'info.json', 'w') as f:
                        json.dump(info, f, indent=4)

def update_readme():
    with open(README_FILE, 'w') as f:
        f.write("# Kattis Solutions\n\n")
        f.write("This repository is where I share solutions to problems from [Kattis](https://open.kattis.com/) as I learn C++. It's a mix of challenge and fun, and I'm excited to see where this journey takes me. Updates will come as I solve more problems. If a solution is wrong/incorrect or you would like to provide suggestions, please contact me on discord `plotsu`.\n\n")
        f.write("## Problems\n")
        f.write("| Problem | Difficulty | Language | Solution |\n")
        f.write("| ------- | ---------- | -------- | -------- |\n")
        
        for lang_dir, language in [(C_DIR, 'C'), (CPP_DIR, 'C++')]:
            for difficulty_dir in sorted(lang_dir.iterdir()):
                difficulty_display = difficulty_dir.stem.replace('1_', '').replace('2_', '').replace('3_', '')
                for file in sorted(difficulty_dir.glob('*.*')):
                    if file.is_file() and not file.name.startswith('.gitkeep'):
                        problem_name = file.stem
                        github_solution_url = f"https://github.com/ImPlotting/Kattis-Solutions/blob/main/Kattis/{lang_dir.name}/{difficulty_dir.stem}/{file.name}"
                        kattis_problem_url = f"https://open.kattis.com/problems/{problem_name.lower()}"
                        f.write(f"| [{problem_name}]({kattis_problem_url}) | {difficulty_display} | {language} | [Solution]({github_solution_url}) |\n")

if __name__ == "__main__":
    move_new_problems()
    update_readme()