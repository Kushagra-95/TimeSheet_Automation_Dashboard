import { useState } from "react";

import Header from "../components/Header";
import StatusCard from "../components/StatusCard";
import ProgressSection from "../components/ProgressSection";
import Console from "../components/Console";
import WorkflowTimeline from "../components/WorkflowTimeline";
import OutputFiles from "../components/OutputFiles";
import HistoryCard from "../components/HistoryCard";
import FileUpload from "../components/FileUpload";

import {
    FiActivity,
    FiCpu,
    FiClock,
    FiCheckCircle
} from "react-icons/fi";

import { runWorkflow , uploadFile} from "../services/workflowApi";

function Dashboard() {

    const [status, setStatus] = useState("Ready");

    const [progress, setProgress] = useState(0);

    const [logs, setLogs] = useState("");

    const [time, setTime] = useState("--");

    const [currentStep, setCurrentStep] = useState(-1);

    const [completed, setCompleted] = useState([false, false]);

    const [files, setFiles] = useState([]);

    const [file, setFile] = useState(null);

    const [jobId, setJobId] = useState(null);
    const handleRun = async () => {
        if (!file) {
    alert("Please select a file.");
    return;
  }
  setStatus("Running");

  setProgress(0);

  setLogs("");

  setCompleted([false, false]);

  setFiles([]);

  const start = Date.now();

  try {
    // await uploadFile(file);
    // const data = await runWorkflow();
    // console.log(data);
    const uploadResult = await uploadFile(file);

setJobId(uploadResult.jobId);

const data = await runWorkflow(uploadResult.jobId);
    let output = "";

    const done = [false, false];

    for (let i = 0; i < data.results.length; i++) {

      setCurrentStep(i);

      await new Promise(resolve => setTimeout(resolve, 800));

      output += `▶ ${data.results[i].script}\n`;

      output += `${data.results[i].output}\n\n`;

      done[i] = true;

      setCompleted([...done]);

      setLogs(output);

      setProgress(((i + 1) / data.results.length) * 100);
    }

    setCurrentStep(-1);

    setStatus("Completed");

    setFiles(data.items);

    setTime(((Date.now() - start) / 1000).toFixed(2) + " sec");

  } catch (err) {

    setStatus("Failed");

    setLogs(err.message);

  }

};

    return (

        <>

            <Header />

            <div className="status-grid">

                <StatusCard

                    title="Workflow"

                    value={status}

                    icon={<FiActivity />}

                />

                <StatusCard

                    title="Scripts"

                    value="1"

                    icon={<FiCpu />}

                />

                <StatusCard

                    title="Execution"

                    value={time}

                    icon={<FiClock />}

                />

                <StatusCard

                    title="Result"

                    value={status === "Completed" ? "Success" : "--"}

                    icon={<FiCheckCircle />}

                />

            </div>
           <div className="trio">
            <div className="upload-panel">

            <FileUpload
                file={file}
                setFile={setFile}
            />
            </div>
            <div className="progress-panel">

            <ProgressSection progress={progress} />
            </div>
</div>
            <div className="action workflow-action">

                <button

                    className="run-btn"
                    
                    onClick={handleRun}

                >

                    ▶ Run Workflow

                </button>

            </div>
            <Console logs={logs} />
            <div className="dashboard-grid">

            <WorkflowTimeline
                currentStep={currentStep}
                completed={completed}
            />

            <OutputFiles
    files={files}
    jobId={jobId}
/>
           {/* <HistoryCard/> */}

        </div>

        </>

    );

}

export default Dashboard;