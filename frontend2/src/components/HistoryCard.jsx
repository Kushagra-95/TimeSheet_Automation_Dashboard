function HistoryCard({ status, duration }) {
  return (
    <div className="history-card">

      <h3>Last Execution</h3>

      <div className="history-row">
        <span>Status</span>

        <strong>{status}</strong>
      </div>

      <div className="history-row">
        <span>Duration</span>

        <strong>{duration}</strong>
      </div>

    </div>
  );
}

export default HistoryCard;