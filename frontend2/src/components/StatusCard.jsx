import { FiTrendingUp } from "react-icons/fi";

function StatusCard({ title, value, icon }) {
    return (
        <div className="status-card">

            <div>

                <p>{title}</p>

                <h2>{value}</h2>

            </div>

            <div className="card-icon">

                {icon || <FiTrendingUp />}

            </div>

        </div>
    );
}

export default StatusCard;