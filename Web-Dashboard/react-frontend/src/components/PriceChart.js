import React from "react";
import {
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

function formatTime(dt) {
  if (!dt) return "";
  const d = new Date(dt);
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

export function PriceChart({ stocks }) {
  const data = stocks.map((s) => ({
    time: formatTime(s.datetime),
    close: s.close_price ? parseFloat(s.close_price).toFixed(2) : null,
    predicted: s.predicted_close ? parseFloat(s.predicted_close).toFixed(2) : null,
    ma5: s.ma_5 ? parseFloat(s.ma_5).toFixed(2) : null,
  }));

  return (
    <div className="chart-card">
      <h2 className="chart-title">AAPL Price</h2>
      <ResponsiveContainer width="100%" height={260}>
        <ComposedChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.15)" />
          <XAxis dataKey="time" tick={{ fill: "#ccc", fontSize: 11 }} interval="preserveStartEnd" />
          <YAxis
            domain={["auto", "auto"]}
            tick={{ fill: "#ccc", fontSize: 11 }}
            tickFormatter={(v) => `$${v}`}
          />
          <Tooltip
            contentStyle={{ background: "rgba(20,30,50,0.95)", border: "1px solid #444", color: "#fff" }}
            formatter={(value, name) => [`$${value}`, name]}
          />
          <Legend wrapperStyle={{ color: "#ccc", fontSize: 13 }} />
          <Line
            type="monotone"
            dataKey="close"
            name="Close"
            stroke="#4f9cff"
            dot={false}
            strokeWidth={2}
            connectNulls
          />
          <Line
            type="monotone"
            dataKey="predicted"
            name="Predicted"
            stroke="#ff9c4f"
            dot={false}
            strokeWidth={2}
            strokeDasharray="5 3"
            connectNulls
          />
          <Line
            type="monotone"
            dataKey="ma5"
            name="MA(5)"
            stroke="#4fff9c"
            dot={false}
            strokeWidth={1.5}
            connectNulls
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
