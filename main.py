import json
import os
from difflib import get_close_matches
from typing import List

def load_knowledge_base(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {"question": []}
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> str or None:
    matches: List[str] = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str or None:
    for q in knowledge_base["question"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match: str or None = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print('Bot: I don’t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["question"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()
