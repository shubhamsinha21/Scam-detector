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
import {
  CheckCircle,
  Error,
  Link as LinkIcon,
  Description,
} from "@mui/icons-material";

const Home = () => {
  // ------------------- states -------------------------

  const [url, setUrl] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [file, setFile] = useState(null);
  const [fileResult, setFileResult] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState(false);
  const [snackbarSeverity, setSnackbarSeverity] = useState("info");
  const [loadingFile, setLoadingFile] = useState(false);

  const showSnackbar = (message, severity) => {
    setSnackbarMessage(message);
    setSnackbarMessage(severity);
    setOpenSnackbar(true);
  };

  // ------------------- Url detection -------------------------

  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", {
        url,
      });
      const result = response.data;
      setPrediction(result);
      showSnackbar(
        `Prediction: ${result.prediction} (${result.confidence})`,
        result.prediction === "scam" ? "error" : "success"
      );
    } catch (err) {
      showSnackbar("Error predicting URL", "error");
    }
  };

  // ------------------- File detection -------------------------

  const handleFileSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      showSnackbar("Please select a file", "error");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoadingFile(true);
      const response = await axios.post(
        "http://127.0.0.1:5000/scam",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setFileResult(response.data);
      showSnackbar(
        `File Prediction: ${response.data.prediction}`,
        response.data.prediction === "scam" ? "error" : "sucess"
      );
    } catch (err) {
      showSnackbar("File upload failed", "error");
    } finally {
      setLoadingFile(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box>{/* Url detetion */}</Box>
    </Container>
  );
};

export default Home;
