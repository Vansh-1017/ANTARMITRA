from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf

class MoodAnalyzer:
    def __init__(self):
        print("Loading pitch-perfect local AI model directly... (Bypassing pipeline bug)")
        # 1. Load the tokenizer (turns words into numbers)
        self.tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
        # 2. Load the core TensorFlow model directly
        self.model = TFAutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
        print("Model loaded successfully!")

    def calculate_mood_score(self, text):
        """
        Analyzes the text for 7 distinct emotions and mathematically 
        calculates a pitch-perfect 1-10 mood score.
        """
        # 1. Convert text to tensor format for the neural network
        inputs = self.tokenizer(text, return_tensors="tf", truncation=True, max_length=512)
        
        # 2. Run the text through the local model
        outputs = self.model(inputs)
        
        # 3. Apply softmax to get the exact probability percentages for each emotion
        probabilities = tf.nn.softmax(outputs.logits, axis=-1)[0].numpy()
        
        # The model's internal labels (0 through 6)
        labels = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
        
        # Our custom 1-10 weights
        emotion_weights = {
            'joy': 10.0,
            'surprise': 7.0,
            'neutral': 5.5,
            'sadness': 3.0,
            'fear': 2.0,
            'anger': 2.0,
            'disgust': 1.0
        }

        weighted_score = 0.0
        
        # 4. Calculate the final score
        for i, prob in enumerate(probabilities):
            emotion = labels[i]
            weighted_score += emotion_weights[emotion] * float(prob)

        # 5. Round to 1 decimal place and ensure bounds
        final_score = round(weighted_score, 1)
        return max(1.0, min(10.0, final_score))

# Quick test to prove it works
if __name__ == "__main__":
    analyzer = MoodAnalyzer()
    
    test_text_1 = "I lost my game today and feel terrible."
    test_text_2 = "I didn't technically win, but I played my absolute best and feel proud."
    test_text_3 = "I am so incredibly angry and frustrated with my team."
    
    print(f"\nText: '{test_text_1}' -> Score: {analyzer.calculate_mood_score(test_text_1)}/10")
    print(f"Text: '{test_text_2}' -> Score: {analyzer.calculate_mood_score(test_text_2)}/10")
    print(f"Text: '{test_text_3}' -> Score: {analyzer.calculate_mood_score(test_text_3)}/10")