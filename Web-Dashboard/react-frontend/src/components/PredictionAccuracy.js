import React from "react";

export function PredictionAccuracy({ stocks }) {
  // Find the most recent entry that has both an actual close and a previous prediction
  const latest = stocks.length > 0 ? stocks[stocks.length - 1] : null;
  const previous = stocks.length > 1 ? stocks[stocks.length - 2] : null;

  const predicted = previous?.predicted_close;
  const actual = latest?.close_price;

  let error = null;
  let errorPct = null;
  if (predicted !== null && predicted !== undefined && actual !== null && actual !== undefined) {
    error = parseFloat(actual) - parseFloat(predicted);
    errorPct = Math.abs(error / parseFloat(actual)) * 100;
  }

  const currentClose = latest ? parseFloat(latest.close_price).toFixed(4) : "—";
  const currentPred = latest?.predicted_close
    ? parseFloat(latest.predicted_close).toFixed(4)
    : "—";

  return (
    <div className="stat-card">
      <h2 className="chart-title">ML Prediction</h2>
      <div className="pred-row">
        <span className="pred-label">Current Close</span>
        <span className="pred-value" style={{ color: "#4f9cff" }}>${currentClose}</span>
      </div>
      <div className="pred-row">
        <span className="pred-label">Next Predicted</span>
        <span className="pred-value" style={{ color: "#ff9c4f" }}>${currentPred}</span>
      </div>
      {errorPct !== null && (
        <div className="pred-row">
          <span className="pred-label">Last Error</span>
          <span
            className="pred-value"
            style={{ color: errorPct < 0.1 ? "#4fff9c" : errorPct < 0.5 ? "#ff9c4f" : "#ff5c5c" }}
          >
            {errorPct.toFixed(3)}%
          </span>
        </div>
      )}
    </div>
  );
}
