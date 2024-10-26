def get_model_by_quality(index):
    # Models arranged by quality/accuracy
    model_names = [
        "llama3-70b-8192",
        "llama3-groq-70b-8192-tool-use-preview",
        "llama-3.1-70b-versatile",
        "llama-3.2-90b-text-preview",
        "llama-3.2-90b-vision-preview",
        "gemma2-9b-it",
        "llama3-8b-8192",
        "llama-3.1-8b-instant",
        "llama3-groq-8b-8192-tool-use-preview",
        "llama-guard-3-8b",
        "llava-v1.5-7b-4096-preview",
        "gemma-7b-it",
        "llama-3.2-11b-text-preview",
        "llama-3.2-11b-vision-preview",
        "llama-3.2-3b-preview",
        "llama-3.2-1b-preview",
        "mixtral-8x7b-32768"
    ]
    
    if 0 <= index < len(model_names):
        return model_names[index]
    else:
        return "Index out of range"

# Usage
# print(get_model_by_quality(0))  # Outputs: llama3-70b-8192
# print(get_model_by_quality(5))  # Outputs: gemma2-9b-it



