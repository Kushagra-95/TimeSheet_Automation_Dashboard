import { useEffect, useRef } from "react";

function Console({ logs, isRunning }) {
  const preRef = useRef(null);

  useEffect(() => {
    if (preRef.current) {
      preRef.current.scrollTop = preRef.current.scrollHeight;
    }
  }, [logs]);

  const renderLogs = (rawLogs) => {
    if (!rawLogs) return null;
    return rawLogs.split("\n").map((line, i) => {
      let cls = "";
      if (line.startsWith("▶"))        cls = "log-script";
      else if (/error|fail/i.test(line)) cls = "log-error";
      else if (/done|success|complete/i.test(line)) cls = "log-success";
      return (
        <span key={i} className={cls}>
          {line}{"\n"}
        </span>
      );
    });
  };

  return (
    <div className="console-card">
      <div className="console-header">
        <span className="red" />
        <span className="yellow" />
        <span className="green" />
        <h3>Execution Console</h3>
        {isRunning && <span className="console-cursor" />}
      </div>

      <pre ref={preRef}>
        {logs
          ? renderLogs(logs)
          : <span className="log-waiting">Waiting for workflow to start…</span>
        }
      </pre>
    </div>
  );
}

export default Console;