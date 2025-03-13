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
import { CheckCircle, Error, Info, Link as LinkIcon, Description } from "@mui/icons-material";

function App() {
  const [url, setUrl] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [file, setFile] = useState(null);
  const [fileResult, setFileResult] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState("info"); // "success", "error", "info"

  // Show snackbar notification
  const showSnackbar = (message, severity) => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setOpenSnackbar(true);
  };

  // Handle URL Scam Detection
  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", { url });
      setPrediction(response.data.predicted);
      showSnackbar(`Prediction: ${response.data.predicted}`, "info");
    } catch (error) {
      console.log("Error", error);
      showSnackbar("Error in prediction", "error");
    }
  };

  // Handle File Scam Detection
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
      setFileResult(response.data.message);
      showSnackbar(`Result: ${response.data.message}`, "info");
    } catch (error) {
      console.log("File upload error", error);
      showSnackbar("File upload failed", "error");
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Paper elevation={3} sx={{ p: 4, width: "100%", textAlign: "center" }}>
          <Typography variant="h3" gutterBottom fontWeight="bold">
            Scam Detector <Info color="primary" />
          </Typography>

          {/* URL Detection */}
          <Typography variant="h5" gutterBottom fontWeight="bold">
            Scam URL Detection
          </Typography>
          <form onSubmit={handleUrlSubmit}>
            <TextField
              fullWidth
              label="Enter URL"
              variant="outlined"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
              sx={{ mb: 2 }}
              inputProps={{ style: { fontSize: "18px", fontWeight: "bold" } }}
            />
            <Button variant="contained" color="primary" type="submit" fullWidth sx={{ fontSize: "18px", fontWeight: "bold" }}>
              Classify
            </Button>
          </form>

          {/* Show Prediction & URL */}
          {prediction && (
            <Box sx={{ mt: 2, textAlign: "center" }}>
              <Typography sx={{ display: "flex", alignItems: "center", gap: 1 }} fontWeight="bold" fontSize="20px">
                {prediction.includes("Scam") ? <Error color="error" /> : <CheckCircle color="success" />}
                Prediction: {prediction}
              </Typography>
              <Typography variant="body1" sx={{ mt: 1, fontWeight: "bold", fontSize: "16px", color: "gray", display: "flex", alignItems: "center", gap: 1 }}>
                <LinkIcon color="action" /> URL: {url}
              </Typography>
            </Box>
          )}

          {/* File Detection */}
          <Typography variant="h5" gutterBottom sx={{ mt: 4 }} fontWeight="bold">
            Scam File Detection
          </Typography>
          <form onSubmit={handleFileSubmit}>
            <Button variant="contained" component="label" fullWidth sx={{ fontSize: "18px", fontWeight: "bold" }}>
              Upload File
              <input
                type="file"
                hidden
                onChange={(e) => setFile(e.target.files[0] || null)}
                required
              />
            </Button>
            <Button
              variant="contained"
              color="secondary"
              type="submit"
              fullWidth
              sx={{ mt: 2, fontSize: "18px", fontWeight: "bold" }}
            >
              Analyze File
            </Button>
          </form>

          {/* Show File Result & Name */}
          {fileResult && (
            <Box sx={{ mt: 2, textAlign: "center" }}>
              <Typography sx={{ display: "flex", alignItems: "center", gap: 1 }} fontWeight="bold" fontSize="20px">
                {fileResult.includes("Scam") ? <Error color="error" /> : <CheckCircle color="success" />}
                Result: {fileResult}
              </Typography>
              {file && (
                <Typography variant="body1" sx={{ mt: 1, fontWeight: "bold", fontSize: "16px", color: "gray", display: "flex", alignItems: "center", gap: 1 }}>
                  <Description color="action" /> File: {file.name}
                </Typography>
              )}
            </Box>
          )}
        </Paper>
      </Box>

      {/* Snackbar for Notifications */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={4000} // Longer duration
        onClose={() => setOpenSnackbar(false)}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }} // Pop up at bottom-center
      >
        <Alert severity={snackbarSeverity} onClose={() => setOpenSnackbar(false)} sx={{ fontSize: "18px", fontWeight: "bold" }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default App;
