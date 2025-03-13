"""
Here, we are using flask as backend
In bet, python main and flask app, we create a communication bridge bet frontend & backend
"""
from flask import Flask, jsonify, request
# render_template is for connection bet frontend & backend
# request - for creating request to frontend for data
import PyPDF2 # for extracting text from pdf
import os # inbuilt module
from google.generativeai import configure, GenerativeModel# for generative ai model
from dotenv import load_dotenv
from flask_cors import CORS


# load env variables
load_dotenv()

# flask app
app = Flask(__name__) # flast has this name parameter
CORS(app) # enable CORS for frontend-backend communication

# set up the Google GenerativeAI api key
api_key = os.getenv("GOOGLE_API_KEY")
configure(api_key=api_key)

# initialize the gemini model
model = GenerativeModel("gemini-1.5-flash")  # calling GenerativeModel from genai

# function to predict text(content) is real/fake
"""
extracted text is provided to predict function
"""
def predict_fake_real_content(text):
    prompt = f"""
    You are an expert in identifying scam messages in text, email, etc.
    
    Analyze the given text and classify it as:
    
    - **Real/Legitimate** (Authentic, safe message)
    - **Scame/Fake** (Phishing, fraud or suspicious message)
    
    **Text to analyze:**
    {text}
    
    **Return a clear message indicating whether this content is real or fake(scam)
    If it is a scam, mention why it seems fraudulent. If it's real, consider it as legitimate.**
    
    **Only return the classification message and nothing else.**
    Note: Don't return empty or null, you only need to return message for the input text
    
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()


# function for url detection
def url_detection(url):
    prompt = f"""
    You are an advanced AI model specalizing in URL security classification. 
    
    Analyze the give url and classify it as:
    
    - Safe URL** : Safe, trusted and non-malicious websites such as google.com, wikipedia.org, amazon.com.
    - Fraud URL** : Fraudulent websites designed to steal personal information. It includes mispelled domains.
    - Malware** : URLs that distribute viruses, ransomware or malicious software. Often includes atomatic downloads.
    - Defacement** : Hacked or defaced websites that display unauthorized content, usually altered by attackers.
    
    **Example URLs and Classification:**
    - **Safe**: "https://www.microsoft.com/"
    - **Fraud**: "http://secure-login.paypal1.com/"
    - **Malware**: "http://free-download-software.xyz/"
    - **Defacement**: "http://hacked-website.com/"

    **Input URL:** {url}
    
    **Output Formats:**
    - Return only a string class name with correct emoji for representing it and enure each cases must have different emojis
    - Example output for a phishing site:
    
    Analyze the URL and return the correct classification (only name in lowercase such as fake, etc)
    Note: Don't retutn empty or null, at any cost return thr corrected class
    
    """

    response  = model.generate_content(prompt)
    return response.text

# adding routes for connecting main and index
@app.route("/scam", methods=['POST'])
def detect_scam():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded !"}), 400
    
    file = request.files['file']
    print(file)
    
    # check user uploaded txt or pdf file
    if file.filename.endswith(".pdf"):
        """
        store data of file
        """
        pdf_reader = PyPDF2.PdfReader(file) # calling PdfReader from pyPDF2, to read file
        extracted_text = [] # variable which will later contain text
        
        # list comprehension
        """
        " " .join([page.extract_text() for page in pdf_reader.pages if page.extract_text()]) - one liner function
        """
        for page in pdf_reader.pages: # calling pages (built in function from pdf_reader)
            if page.extract_text(): # extract_text() is an inbuilt function
                text = page.extract_text() # extracting text and assigning into variable
                if text:
                    extracted_text.append(text)
        
        extracted_text = " ".join(extracted_text)
    # print(extracted_text)
    
    elif file.filename.endswith(".txt"):
        extracted_text = file.read().decode("utf-8") # reading text file and decoding it into fixed format
        
    else:
        return jsonify({"error": "Invalid file format ! Only .pdf and .txt file  supported !"})
    
    # print(extracted_text)
    message = predict_fake_real_content(extracted_text) # provided text in the function
    
    return jsonify({"message": message})


@app.route("/predict", methods=["POST"])
def detect_url():
    data = request.get_json()
    url = data.get("url", " ").strip() # get a url and removing whitespaces
    
    # check the content is url or not   
    if not url.startswith(("http://", "https://")): # startswith need a tuple for multiple args
        return jsonify({"error": "Invalid URL format!"}), 400
    
    classification = url_detection(url) # calling url_detection function and assigned in a variable
    return jsonify({"predicted": classification})
    
"""
we will first extract text from pdf or txt file 
and then the model will detect it
"""
    
# python main
if __name__ == "__main__":
    app.run(debug=True) # run the app
    
    
# jsonify -> is a function in flask that converts python dict (lists) into JSON responses for APIs
# sets headers
