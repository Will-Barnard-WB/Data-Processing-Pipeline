import { useEffect, useState } from "react";
import { io } from "socket.io-client";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:5050";

export function useStockSocket() {
  const [stocks, setStocks] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socket = io(BACKEND_URL, { transports: ["websocket", "polling"] });

    socket.on("connect", () => setIsConnected(true));
    socket.on("disconnect", () => setIsConnected(false));
    socket.on("stock_update", (data) => {
      setStocks((prev) => [...prev.slice(-49), data]);
    });

    return () => socket.disconnect();
  }, []);

  return { stocks, isConnected };
}
