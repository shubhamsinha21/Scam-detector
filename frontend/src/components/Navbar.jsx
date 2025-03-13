import { AppBar, Toolbar, Typography, IconButton } from "@mui/material";
import { Brightness4, Brightness7, Block } from "@mui/icons-material";

const Navbar = ({ darkMode, toggleDarkMode }) => {
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h4" fontWeight="bold" sx={{ flexGrow: 1, display: "flex", alignItems: "center" }}>
          <Block sx={{ fontSize: 40, mr: 1 }} /> Scam Detector
        </Typography>
        <IconButton color="inherit" onClick={toggleDarkMode}>
          {darkMode ? <Brightness7 /> : <Brightness4 />}
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
