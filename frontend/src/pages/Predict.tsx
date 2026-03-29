import { useState } from "react";
import { predict } from "../api/predict";

const Predict = () => {
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);

    try {
      const data = {
        f1: 1,
        f2: 2,
        f3: 3,
        f4: 4,
        f5: 5,
      };

      const res = await predict(data);

      if (res && res.result !== undefined) {
        alert("PCOS Prediction: " + res.result);
      } else {
        alert("No result from backend");
      }

    } catch (err) {
      alert("Failed to connect backend");
    }

    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Predict Page</h1>

      <button onClick={handlePredict} disabled={loading}>
        {loading ? "Predicting..." : "Predict"}
      </button>
    </div>
  );
};

export default Predict;