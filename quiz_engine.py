import time

class QuizBot:
    def __init__(self):
        self.user_data = {}

    def start_session(self, user_id, questions):
        self.user_data[user_id] = {
            "qs": questions,
            "idx": 0,
            "score": 0,
            "start": time.time(),
            "history": []
        }
    
    def get_current_q(self, user_id):
        data = self.user_data.get(user_id)
        if data and data["idx"] < len(data["qs"]):
            return data["qs"][data["idx"]]
        return None

    def save_answer(self, user_id, user_answer):
        data = self.user_data[user_id]
        current_q = data["qs"][data["idx"]]
        is_correct = (user_answer.strip().lower() == current_q['correct'].strip().lower())
        
        if is_correct: data["score"] += 1
            
        data["history"].append({
            "q": current_q['question'],
            "u": user_answer,
            "c": current_q['correct'],
            "is_correct": is_correct
        })
        data["idx"] += 1
        return is_correct

quiz_engine = QuizBot()
