import { useEffect, useState } from "react";
import logo from "../assets/nagarro_black.png";

function Header({ status = "Ready" }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const statusClass = {
    Running:   "running",
    Completed: "completed",
    Failed:    "failed",
  }[status] || "";

  const statusLabel = {
    Ready:     "Idle",
    Running:   "Processing",
    Completed: "Completed",
    Failed:    "Error",
  }[status] || status;

  return (
    <header className="top-header">
      <div className="top-left">
        <img src={logo} alt="Nagarro" className="top-logo" />
      </div>

      <div className="top-center">
        <h2>Timesheet Automation Dashboard</h2>
        <p>Workflow Tracker &amp; Output Monitor</p>
      </div>

      <div className="top-right">
        <div className={`header-status-badge ${statusClass}`}>
          <span className="dot" />
          {statusLabel}
        </div>

        <div className="time-box">
          <span>{time.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })}</span>
          <span>{time.toLocaleTimeString()}</span>
        </div>
      </div>
    </header>
  );
}

export default Header;