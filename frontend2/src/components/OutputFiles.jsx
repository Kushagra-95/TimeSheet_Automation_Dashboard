import {
  FiDownload,
  FiFileText,
  FiFolder,
} from "react-icons/fi";

import {
  downloadFile,
  downloadFolder,
} from "../services/workflowApi";

function OutputFiles({ files, jobId }) {
  const handleFileDownload = async (fileName) => {
  try {
    const blob = await downloadFile(fileName, jobId);

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(error);
    alert("Failed to download file.");
  }
};

 const handleFolderDownload = async (folderName) => {
  try {
    const blob = await downloadFolder(folderName, jobId);

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = `${folderName}.zip`;

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(error);
    alert("Failed to download folder.");
  }
};

  return (
    <div className="output-card">
      <h3>Generated Files</h3>

      {!files || files.length === 0 ? (
        <p className="empty">No files generated</p>
      ) : (
        files.map((item) => (
          <div className="file-item" key={item.name}>
            {item.type === "file" ? <FiFileText /> : <FiFolder />}

            <span>{item.name}</span>

            <button
              className="download-btn"
              onClick={() =>
                item.type === "file"
                  ? handleFileDownload(item.name)
                  : handleFolderDownload(item.name)
              }
            >
              <FiDownload />
            </button>
          </div>
        ))
      )}
    </div>
  );
}

export default OutputFiles;