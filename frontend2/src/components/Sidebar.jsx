import { useState } from "react";
import {
  FiHome,
  FiPlayCircle,
  FiFolder,
  FiClock,
  FiSettings,
  FiMenu,
} from "react-icons/fi";

import logo from "../assets/nagarro-logo-png_seeklogo-572171.png";

function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={collapsed ? "sidebar collapsed" : "sidebar"}>

      <button
        className="menu-btn"
        onClick={() => setCollapsed(!collapsed)}
      >
        <FiMenu />
      </button>

      <div className="logo-section">
        {/* <h2 style={{ color: "#4DE1C1" }}>Timesheet</h2> */}
        {!collapsed && <img src={logo} alt="logo" />}
      </div>

      <nav>

        <a className="active">

          <FiHome />

          {!collapsed && "Dashboard"}

        </a>

        {/* <a>

          <FiPlayCircle />

          {!collapsed && "Workflow"}

        </a>

        <a>

          <FiFolder />

          {!collapsed && "Output"}

        </a>

        <a>

          <FiClock />

          {!collapsed && "History"}

        </a>

        <a>

          <FiSettings />

          {!collapsed && "Settings"}

        </a> */}

      </nav>

    </aside>
  );
}

export default Sidebar;