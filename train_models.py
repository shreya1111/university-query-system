"""
Run once to train and save all ML models.
Usage: python train_models.py
"""
from features.ai.intent_classifier  import train_intent_model
from features.ai.priority_predictor import train_priority_model
from features.ai.sentiment_analysis import train_sentiment_model

if __name__ == "__main__":
    print("Training intent classifier...")
    r = train_intent_model()
    print(f"  ✓ intent model   — accuracy: {r['accuracy']}  samples: {r['samples']}")

    print("Training priority predictor...")
    r = train_priority_model()
    print(f"  ✓ priority model — accuracy: {r['accuracy']}  samples: {r['samples']}")

    print("Training sentiment analyser...")
    r = train_sentiment_model()
    print(f"  ✓ sentiment model — accuracy: {r['accuracy']}  samples: {r['samples']}")

    print("\nAll models saved to models/")