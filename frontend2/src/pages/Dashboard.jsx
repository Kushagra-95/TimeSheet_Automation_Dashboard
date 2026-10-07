import { useState } from "react";
import toast, { Toaster } from "react-hot-toast";

import Header from "../components/Header";
import StatusCard from "../components/StatusCard";
import ProgressSection from "../components/ProgressSection";
import Console from "../components/Console";
import OutputFiles from "../components/OutputFiles";
import FileUpload from "../components/FileUpload";

import {
  FiActivity,
  FiCpu,
  FiClock,
  FiCheckCircle,
} from "react-icons/fi";

import { runWorkflow, uploadFile } from "../services/workflowApi";

function Dashboard() {
  const [status, setStatus]     = useState("Ready");
  const [progress, setProgress] = useState(0);
  const [logs, setLogs]         = useState("");
  const [time, setTime]         = useState("--");
  const [files, setFiles]       = useState([]);
  const [file, setFile]         = useState(null);
  const [jobId, setJobId]       = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  const handleRun = async () => {
    if (!file) {
      toast.error("Please select an Excel file first.");
      return;
    }

    setStatus("Running");
    setIsRunning(true);
    setProgress(0);
    setLogs("");
    setFiles([]);

    const start = Date.now();
    const uploadToast = toast.loading("Uploading file…");

    try {
      const uploadResult = await uploadFile(file);
      toast.dismiss(uploadToast);
      toast.loading("Running workflow…", { id: "workflow" });

      setJobId(uploadResult.jobId);

      const data = await runWorkflow(uploadResult.jobId);
      toast.dismiss("workflow");

      let output = "";
      for (let i = 0; i < data.results.length; i++) {
        await new Promise((r) => setTimeout(r, 800));
        output += `▶ ${data.results[i].script}\n`;
        output += `${data.results[i].output}\n\n`;
        setLogs(output);
        setProgress(((i + 1) / data.results.length) * 100);
      }

      const elapsed = ((Date.now() - start) / 1000).toFixed(2);
      setStatus("Completed");
      setIsRunning(false);
      setFiles(data.items);
      setTime(`${elapsed}s`);
      toast.success(`Workflow completed in ${elapsed}s`);
    } catch (err) {
      toast.dismiss();
      setStatus("Failed");
      setIsRunning(false);
      setLogs((prev) => prev + `\n[ERROR] ${err.message}`);
      toast.error(`Workflow failed: ${err.message}`);
    }
  };

  return (
    <>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: "#0c1525",
            color: "#e2e8f0",
            border: "1px solid rgba(148,163,184,.15)",
            fontSize: "13px",
          },
          success: { iconTheme: { primary: "#14b8a6", secondary: "#060d1a" } },
          error:   { iconTheme: { primary: "#f87171", secondary: "#060d1a" } },
        }}
      />

      <Header status={status} />

      <div className="dashboard-container">
        {/* Status Cards */}
        <div className="status-grid">
          <StatusCard
            title="Workflow"
            value={status}
            icon={<FiActivity />}
            subtitle={isRunning ? "In progress" : ""}
          />
          <StatusCard
            title="Scripts"
            value="1"
            icon={<FiCpu />}
            subtitle="Generate_Timesheets.py"
          />
          <StatusCard
            title="Execution Time"
            value={time}
            icon={<FiClock />}
            subtitle={status === "Completed" ? "Last run" : ""}
          />
          <StatusCard
            title="Result"
            value={status === "Completed" ? "Success" : status === "Failed" ? "Failed" : "--"}
            icon={<FiCheckCircle />}
            subtitle={files.length > 0 ? `${files.length} file(s) generated` : ""}
          />
        </div>

        {/* Upload + Progress */}
        <div className="trio">
          <div className="upload-panel">
            <FileUpload file={file} setFile={setFile} />
          </div>
          <div className="progress-panel">
            <ProgressSection progress={progress} isRunning={isRunning} />
          </div>
        </div>

        {/* Run Button */}
        <div className="action workflow-action">
          <button
            className={`run-btn ${isRunning ? "running" : ""}`}
            onClick={handleRun}
            disabled={isRunning}
          >
            {isRunning ? "⏳ Running Workflow…" : "▶ Run Workflow"}
          </button>
        </div>

        {/* Console + Output */}
        <div className="console-output-grid">
          <div className="console-panel">
            <Console logs={logs} isRunning={isRunning} />
          </div>
          <div className="output-panel">
            <OutputFiles files={files} jobId={jobId} />
          </div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;