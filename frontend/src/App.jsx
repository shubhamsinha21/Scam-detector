import { createTheme, ThemeProvider, CssBaseline } from "@mui/material";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import { useState } from "react";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const theme = createTheme({
    palette: {
      mode: darkMode ? "dark" : "light",
    },
  });

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      <Home />
    </ThemeProvider>
  );
}

export default App;
