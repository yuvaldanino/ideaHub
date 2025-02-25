import gradio as gr
import whisper
import tempfile
import numpy as np
import scipy.io.wavfile as wav
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load Whisper model (speech-to-text)
whisper_model = whisper.load_model("base")  # Use "small", "medium", or "large" for better accuracy

# Load Flan-T5 model (text-to-outline)
model_name = "google/flan-t5-base"  # You can use "flan-t5-large" for better performance
tokenizer = T5Tokenizer.from_pretrained(model_name)
flan_model = T5ForConditionalGeneration.from_pretrained(model_name)

def transcribe_audio(audio):
    """Convert speech to text using Whisper"""
    if audio is None:
        return "No audio recorded."

    sample_rate, audio_data = audio

    # Save as temporary WAV file
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_wav.name, sample_rate, np.array(audio_data, dtype=np.int16))

    # Transcribe audio
    result = whisper_model.transcribe(temp_wav.name)
    return result["text"]

def generate_outline(text):
    """Generate an outline based on transcribed text"""
    if not text.strip():
        return "No text provided for outline generation."

    # More detailed prompt for structured, insightful outlines
    # prompt = f"""
    # Create a highly detailed and structured bullet-point outline for the following idea:  
    # "{text}"  

    # The outline should include:  
    # - A **clear and concise summary** of the idea  
    # - **Step-by-step implementation plan**  
    # - **Technologies or tools needed** (if applicable)  
    # - **Challenges & solutions**  
    # - **Insights and expert recommendations**  
    # - Any other relevant considerations  
    # """
    prompt = f"Generate a structured bullet-point outline for: {text}"


    print("Prompt:", prompt)  # Debugging: Print the prompt

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    print("Tokenized Inputs:", inputs)  # Debugging: Print the tokenized inputs

    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask

    outputs = flan_model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=1024, repetition_penalty=1.2)
    print("Model Outputs:", outputs)  # Debugging: Print the raw model outputs

    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Decoded Output:", decoded_output)  # Debugging: Print the decoded output

    return decoded_output

def speech_to_outline(audio):
    """Takes recorded speech, transcribes it, and generates an outline"""
    text = transcribe_audio(audio)
    outline = generate_outline(text)
    return text, outline

 #Gradio Interface
iface = gr.Interface(
    fn=speech_to_outline,
    inputs=gr.Audio(type="numpy", label="Record your idea"),
    outputs=[
        gr.Textbox(label="Transcribed Text"),
        gr.Textbox(label=" AI-Generated Outline", lines=20, interactive=True),
    ],
    title="AI Speech TO Outline Generator",
    description="Speak your idea, and this AI will transcribe it and generate a structured, in-depth outline.",
)

iface.launch()
