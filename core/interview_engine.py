from core.question_generator import generate_question, generate_followup, generate_feedback

class InterviewEngine:
    def __init__(self, company, role, difficulty):
        self.company = company
        self.role = role
        self.difficulty = difficulty
        self.history = []
        self.current_question = None
        self.asked_questions = []

    def load_starter_question(self):
        q = generate_question(
            self.company,
            self.role,
            self.difficulty,
            self.asked_questions
        )
        self.current_question = q
        self.asked_questions.append(q)
        return q

    def get_followup(self, user_answer):
        self.history.append({
            "question": self.current_question,
            "answer": user_answer
        })
        
        followup = generate_followup(
            self.company,
            self.role,
            self.current_question,
            user_answer,
            self.history
        )
        
        self.current_question = followup
        self.asked_questions.append(followup)
        return followup

    def get_feedback(self):
        if not self.history:
            return "No interview data found."
        return generate_feedback(self.company, self.role, self.history)

    def total_questions(self):
        return len(self.history)