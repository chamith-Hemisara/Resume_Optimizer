import os
import pdfplumber
import google.generativeai as palm
import spacy
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure Google PaLM API Key
palm.configure(api_key="******************8")

# Load the SpaCy NLP model
nlp = spacy.load('en_core_web_sm')


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Extract text from the uploaded resume
    resume_file = request.files['resume']
    resume_text = extract_text_from_pdf(resume_file)

    # Analyze the resume text using Google PaLM
    review = analyze_with_google_palm(resume_text)

    return jsonify({"resume_text": resume_text, "review": review})


@app.route('/optimize', methods=['POST'])
def optimize_resume():
    resume_text = request.form.get('resume_text')

    if not resume_text:
        return jsonify({"error": "No resume text provided"}), 400

    # Google PaLM analysis for optimization tips
    tips = generate_optimization_tips(resume_text)

    return jsonify({"tips": tips})


# Function to analyze text using Google PaLM and return a list of professional review tips
def analyze_with_google_palm(resume_text):
    prompt = f"Analyze the following resume and provide a professional review, focusing on key strengths, weaknesses, and areas for improvement: {resume_text}"

    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.7,
        max_output_tokens=800
    )

    # Split the response into a list of suggestions
    review = completion.result.split("\n")
    review = [line.strip() for line in review if line.strip()]  # Remove any empty or whitespace-only lines

    return review


# Function to generate optimization tips using Google PaLM, formatted as a list
def generate_optimization_tips(resume_text):
    prompt = f"Based on the following resume, provide specific and actionable tips to improve it: {resume_text}"

    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.7,
        max_output_tokens=800
    )

    tips = completion.result.split("\n")
    tips = [tip.strip() for tip in tips if tip.strip()]  # Clean up any empty lines or excessive whitespace

    return tips


if __name__ == '__main__':
    app.run(debug=True)
