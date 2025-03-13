import { useState } from "react";
import axios from "axios";
import {
  Container,
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Snackbar,
  Alert,
} from "@mui/material";
import { CheckCircle, Error, Link as LinkIcon, Description } from "@mui/icons-material";

const Home = () => {
  const [url, setUrl] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [file, setFile] = useState(null);
  const [fileResult, setFileResult] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState("info");

  const showSnackbar = (message, severity) => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setOpenSnackbar(true);
  };

  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", { url });
      const predictionResult = response.data.predicted.toLowerCase();
      setPrediction(predictionResult);
      showSnackbar(`Prediction: ${response.data.predicted}`, predictionResult.includes("scam") ? "error" : "success");
    } catch (error) {
      showSnackbar("Error in prediction", "error");
    }
  };

  const handleFileSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      showSnackbar("Please select a file", "error");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/scam", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const filePrediction = response.data.message.toLowerCase();
      setFileResult(filePrediction);
      showSnackbar(`Result: ${response.data.message}`, filePrediction.includes("scam") ? "error" : "success");
    } catch (error) {
      showSnackbar("File upload failed", "error");
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ minHeight: "100vh", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
        <Paper elevation={3} sx={{ p: 4, width: "100%", textAlign: "center" }}>

          {/* URL Detection */}
          <Typography variant="h5" gutterBottom fontWeight="bold">
            Scam URL Detection
          </Typography>
          <form onSubmit={handleUrlSubmit}>
            <TextField fullWidth label="Enter URL" value={url} onChange={(e) => setUrl(e.target.value)} required sx={{ mb: 2 }} />
            <Button variant="contained" color="primary" type="submit" fullWidth>
              Classify
            </Button>
          </form>

          {prediction && (
            <Box sx={{ mt: 2, textAlign: "center" }}>
              <Typography fontWeight="bold" fontSize="20px" sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                {prediction.includes("fraud") ? <Error color="error" /> : <CheckCircle color="success" />} Prediction: {prediction}
              </Typography>
              <Typography sx={{ mt: 1, fontWeight: "bold", fontSize: "16px", color: "gray", display: "flex", alignItems: "center", gap: 1 }}>
                <LinkIcon color="action" /> URL: {url}
              </Typography>
            </Box>
          )}

          {/* File Detection */}
          <Typography variant="h5" gutterBottom sx={{ mt: 4 }} fontWeight="bold">
            Scam File Detection
          </Typography>
          <form onSubmit={handleFileSubmit}>
            <Button variant="contained" component="label" fullWidth>
              Upload File
              <input type="file" hidden onChange={(e) => setFile(e.target.files[0] || null)} required />
            </Button>
            <Button variant="contained" color="secondary" type="submit" fullWidth sx={{ mt: 2 }}>
              Analyze File
            </Button>
          </form>

          {fileResult && (
            <Box sx={{ mt: 2, textAlign: "center" }}>
              <Typography fontWeight="bold" fontSize="20px" sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                {fileResult.includes("scam") ? <Error color="error" /> : <CheckCircle color="success" />} Result: {fileResult}
              </Typography>
              {file && (
                <Typography sx={{ mt: 1, fontWeight: "bold", fontSize: "16px", color: "gray", display: "flex", alignItems: "center", gap: 1 }}>
                  <Description color="action" /> File: {file.name}
                </Typography>
              )}
            </Box>
          )}
        </Paper>
      </Box>

      <Snackbar open={openSnackbar} autoHideDuration={4000} onClose={() => setOpenSnackbar(false)} anchorOrigin={{ vertical: "bottom", horizontal: "center" }}>
        <Alert severity={snackbarSeverity} onClose={() => setOpenSnackbar(false)}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Home;
