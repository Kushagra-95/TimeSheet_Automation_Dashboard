import { useState } from "react";
import {
  FiDownload,
  FiFileText,
  FiFolder,
  FiLoader,
  FiInbox,
} from "react-icons/fi";
import { downloadFile, downloadFolder } from "../services/workflowApi";

function OutputFiles({ files, jobId }) {
  const [downloading, setDownloading] = useState({});

  const triggerDownload = (blob, name) => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const handleFileDownload = async (fileName) => {
    setDownloading((d) => ({ ...d, [fileName]: true }));
    try {
      const blob = await downloadFile(fileName, jobId);
      triggerDownload(blob, fileName);
    } catch {
      alert("Failed to download file.");
    } finally {
      setDownloading((d) => ({ ...d, [fileName]: false }));
    }
  };

  const handleFolderDownload = async (folderName) => {
    setDownloading((d) => ({ ...d, [folderName]: true }));
    try {
      const blob = await downloadFolder(folderName, jobId);
      triggerDownload(blob, `${folderName}.zip`);
    } catch {
      alert("Failed to download folder.");
    } finally {
      setDownloading((d) => ({ ...d, [folderName]: false }));
    }
  };

  const isEmpty = !files || files.length === 0;

  return (
    <div className="output-card">
      <div className="output-card-header">
        <h4>Generated Files</h4>
        {!isEmpty && (
          <span className="output-file-count">{files.length}</span>
        )}
      </div>

      <div className="generated-files-list">
        {isEmpty ? (
          <div className="empty-state">
            <FiInbox />
            <p>No output files yet</p>
            <span>Run the workflow to generate timesheets</span>
          </div>
        ) : (
          files.map((item) => (
            <div
              className={`file-item ${item.type === "folder" ? "folder-item" : ""}`}
              key={item.name}
            >
              {item.type === "file" ? <FiFileText /> : <FiFolder />}
              <span title={item.name}>{item.name}</span>
              <button
                className="download-btn"
                title={`Download ${item.type === "folder" ? "as ZIP" : "file"}`}
                onClick={() =>
                  item.type === "file"
                    ? handleFileDownload(item.name)
                    : handleFolderDownload(item.name)
                }
                disabled={downloading[item.name]}
              >
                {downloading[item.name]
                  ? <FiLoader style={{ animation: "spin 1s linear infinite" }} />
                  : <FiDownload />
                }
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default OutputFiles;