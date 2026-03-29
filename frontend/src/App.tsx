import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import LogCycle from "./pages/LogCycle";
import RiskAssessment from "./pages/RiskAssessment";
import History from "./pages/History";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/log-cycle" element={<LogCycle />} />
        <Route path="/risk-assessment" element={<RiskAssessment />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;