function ProgressSection({ progress, isRunning }) {
  const pct = Math.round(progress);

  return (
    <div className="progress-card">
      <div className="progress-header">
        <h3>Workflow Progress</h3>
        <span>{pct}%</span>
      </div>

      <div className="progress-track">
        <div
          className={`progress-fill ${isRunning ? "animating" : ""}`}
          style={{ width: `${pct}%` }}
        />
      </div>

      <div className="progress-steps">
        <span className="progress-step-label">
          {pct === 0 && !isRunning && "Awaiting workflow run"}
          {pct > 0 && pct < 100 && "Processing scripts..."}
          {pct === 100 && "All scripts executed"}
        </span>
      </div>
    </div>
  );
}

export default ProgressSection;