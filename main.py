"""
Here, we are using flask as backend
In bet, python main and flask app, we create a communication bridge bet frontend & backend
"""
from flask import Flask, render_template, request
# render_template is for connection bet frontend & backend
# request - for creating request to frontend for data
import PyPDF2 # for extracting text from pdf
import os # inbuilt module
from google.generativeai import configure, GenerativeModel# for generative ai model
from dotenv import load_dotenv


# load env variables
load_dotenv()

# flask app
app = Flask(__name__) # flast has this name parameter

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


# adding routes for connecting main and index
@app.route("/") # url is empty
def index(): #function 
    return render_template("index.html") # render template is re-directing it to index page

@app.route("/scam", methods=['POST'])
def detect_scam():
    if 'file' not in request.files:
        return render_template("index.html", message="No file uploaded !")
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
        return render_template("index.html", message = "Invalid file format ! Only .pdf and .txt file  supported !")
    
    # print(extracted_text)
    message = predict_fake_real_content(extracted_text) # provided text in the function
    
    return render_template("index.html", message = message)
        
    
"""
we will first extract text from pdf or txt file 
and then the model will detect it
"""
    
# python main
if __name__ == "__main__":
    app.run(debug=True) # run the app
