class ContextTracker:
    def __init__(self):
        self.history = []
    
    def add(self, question, answer):
        self.history.append({"question": question, "answer": answer})
    
    def get_last_n(self, n=3):
        return self.history[-n:]
    
    def get_context_string(self, n=3):
        recent = self.get_last_n(n)
        return " | ".join([f"Q: {h['question']} → A: {h['answer']}" for h in recent])
    
    def clear(self):
        self.history = []
    
    def total_questions(self):
        return len(self.history)