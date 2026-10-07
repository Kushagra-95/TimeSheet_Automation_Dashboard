import { FiTrendingUp } from "react-icons/fi";

function StatusCard({ title, value, icon, subtitle }) {
  return (
    <div className="status-card">
      <div>
        <p>{title}</p>
        <h2>{value}</h2>
        {subtitle && (
          <span style={{ fontSize: "11px", color: "var(--text-subtle)", marginTop: "2px", display: "block" }}>
            {subtitle}
          </span>
        )}
      </div>
      <div className="card-icon">
        {icon || <FiTrendingUp />}
      </div>
    </div>
  );
}

export default StatusCard;