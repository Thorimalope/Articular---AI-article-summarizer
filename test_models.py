from transformers import pipeline

print("Loading model...")

# Load summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Sample text
text = """
Artificial intelligence is transforming industries by enabling machines to learn from data,
identify patterns, and make decisions with minimal human intervention.
It is used in healthcare, finance, transportation, and many other sectors.
"""

# Generate summary
summary = summarizer(text, max_length=50, min_length=20, do_sample=False)

# Print result
print("\nSummary:")
print(summary[0]['summary_text'])