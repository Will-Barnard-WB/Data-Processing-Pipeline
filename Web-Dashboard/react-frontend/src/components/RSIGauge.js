import React from "react";

function rsiColor(rsi) {
  if (rsi === null || rsi === undefined) return "#888";
  if (rsi > 70) return "#ff5c5c";
  if (rsi < 30) return "#4fff9c";
  return "#4f9cff";
}

function rsiLabel(rsi) {
  if (rsi === null || rsi === undefined) return "—";
  if (rsi > 70) return "Overbought";
  if (rsi < 30) return "Oversold";
  return "Neutral";
}

export function RSIGauge({ rsi }) {
  const color = rsiColor(rsi);
  const label = rsiLabel(rsi);
  const display = rsi !== null && rsi !== undefined ? rsi.toFixed(1) : "—";

  return (
    <div className="stat-card">
      <h2 className="chart-title">RSI (14)</h2>
      <div className="rsi-value" style={{ color }}>
        {display}
      </div>
      <div className="rsi-label" style={{ color }}>
        {label}
      </div>
      <div className="rsi-bar-track">
        <div
          className="rsi-bar-fill"
          style={{
            width: rsi !== null ? `${Math.min(rsi, 100)}%` : "0%",
            background: color,
          }}
        />
        <div className="rsi-bar-marker rsi-bar-oversold" />
        <div className="rsi-bar-marker rsi-bar-overbought" />
      </div>
      <div className="rsi-bar-labels">
        <span>0</span>
        <span style={{ marginLeft: "26%" }}>30</span>
        <span style={{ marginLeft: "36%" }}>70</span>
        <span style={{ marginLeft: "auto" }}>100</span>
      </div>
    </div>
  );
}
