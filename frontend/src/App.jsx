import { useState } from "react"  // a react hook for managing state variables
import axios from "axios"  // a library used to send HTTPs requests to the flask backend

function App() {
  // state for url
  const [url, setUrl] = useState("") // url - stores the user-input url
  const [prediction, setPrediction] = useState(null) // stores the scam classification result for url
  const [file, setFile] = useState(null) // stores the uploaded file like (PDF/TXT)
  const [filerResult, setFileResult] = useState(null) // stores the scam detection result for uploaded file

/* 
Handle form submission for url-based scam detection
*/
  const handleUrlSubmit = async (e) => {
    e.preventDefault() // prevents page reload on form submission
    try{
      // send a POST req to the flask backend with the entered URL
      const response = await axios.post("http://127.0.0.1:5000/predict", {url})
      // axios - parses the actual data sent from flash API
      // if sucessful, stores the backend's response

      setPrediction(response.data.predicted)
      // flask return json, axios converts it
    }
    catch (error){
      console.log("Error", error)
    }
  }


/* Handle file-based scam detection */
const handleFileSubmit = async (e) => {
  e.preventDefault()

  const formData = new FormData() // formData - js object allows to create key-value pair, used for hamdlinh file uploads in multipart/form-data format, required when sending files via https req
 // initializes a new instance to store form fields and file uplaods
  formData.append("file", file) // add key value pair , expects in request.files["file"]

  try{
    const response = await axios.post("http://127.0.0.1:5000/scam", formData, {
      headers: {"Content-Type": "multipart/form-data"} // adding headers for file uploads
    })
    setFileResult(response.data.message) // store message
  }
  catch (error){
    console.log("File upload error", error)
  }
}

  return (
    <div>
      <h1>Scam Detector</h1>
      <h2>Scam URL Detection</h2>
      <form onSubmit={handleUrlSubmit}>
        <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} required />
        <button type="submit">Classify</button>
      </form>
      {prediction && <p>Prediction: {prediction}</p>}

      <h2>Scam File Detection</h2>
      <form onSubmit={handleFileSubmit}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} required />
        <button type="submit">Upload</button>
      </form>
      {filerResult && <p>Result: {filerResult}</p>}
    </div>
  )
}

export default App