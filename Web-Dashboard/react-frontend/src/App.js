import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import { useStockSocket } from "./hooks/useStockSocket";
import { PriceChart } from "./components/PriceChart";
import { RSIGauge } from "./components/RSIGauge";
import { PredictionAccuracy } from "./components/PredictionAccuracy";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:5050";

const Dashboard = () => {
  const [initialStocks, setInitialStocks] = useState([]);
  const { stocks: liveStocks, isConnected } = useStockSocket();

  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/`)
      .then((res) => setInitialStocks(res.data.stocks || []))
      .catch(() => {});
  }, []);

  // Seed the chart with historical data on load, then overlay live updates
  const stocks = liveStocks.length > 0 ? liveStocks : initialStocks;
  const latest = stocks.length > 0 ? stocks[stocks.length - 1] : null;

  return (
    <div className="App">
      <h1>AAPL Live Dashboard</h1>
      <div className="status-bar">
        <span className={`status-dot ${isConnected ? "connected" : "disconnected"}`} />
        {isConnected ? "Live" : "Connecting..."}
      </div>

      <PriceChart stocks={stocks} />

      <div className="stats-row">
        <RSIGauge rsi={latest?.rsi_14 ?? null} />
        <PredictionAccuracy stocks={stocks} />
        <div className="stat-card">
          <h2 className="chart-title">Last Close</h2>
          <div className="big-stat" style={{ color: "#4f9cff" }}>
            {latest ? `$${parseFloat(latest.close_price).toFixed(4)}` : "—"}
          </div>
          <div className="big-stat-sub">
            MA(5): {latest?.ma_5 ? `$${parseFloat(latest.ma_5).toFixed(4)}` : "—"}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
