import { useEffect, useState } from "react";
import logo from "../assets/nagarro_black.png";
import { FiUser } from "react-icons/fi";

function Header() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <header className="top-header">
      <div className="top-left">
        <img src={logo} alt="Nagarro" className="top-logo" />
      </div>

      <div className="top-center">
        <h2>Timesheet Automation Dashboard</h2>
        <p>Workflow Tracker & Output Monitor</p>
      </div>

      <div className="top-right">
        <div className="time-box">
          <span>{time.toLocaleDateString()}</span>
          <span>{time.toLocaleTimeString()}</span>
        </div>

        
      </div>
    </header>
  );
}

export default Header;