import { useEffect, useState } from "react";
import logo from "../assets/nagarro_black.png";

function Header() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="header">
      <div className="header-brand">
        <img src={logo} className="brand-logo" alt="Nagarro logo" />
      </div>

      <div className="header-title">
        <h1>Timesheet Automation Dashboard</h1>
        <p>Workflow tracker and output monitor</p>
      </div>

      <div className="header-right">
        <div className="clock">
          {time.toLocaleDateString()} <br />
          {time.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}

export default Header;