import { useState } from "react";
import { FiUploadCloud, FiFileText, FiX } from "react-icons/fi";

function FileUpload({ file, setFile }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") setIsDragging(true);
    else setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped && (dropped.name.endsWith(".xlsx") || dropped.name.endsWith(".xls"))) {
      setFile(dropped);
    }
  };

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="upload-card">
      <label className="upload-label">Upload Timesheet</label>

      <label
        className={`upload-box ${isDragging ? "drag-over" : ""}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <FiUploadCloud className="upload-icon" />
        <div>
          <p className="upload-title">
            {isDragging ? "Drop your file here" : "Click or drag & drop Excel file"}
          </p>
        </div>
        <input
          type="file"
          accept=".xlsx,.xls"
          hidden
          onChange={(e) => setFile(e.target.files[0])}
        />
      </label>

      {file && (
        <div className="selected-file">
          <FiFileText />
          <span>{file.name}</span>
          <span style={{ marginLeft: "auto", opacity: .6, fontSize: "11px", flexShrink: 0 }}>
            {formatSize(file.size)}
          </span>
          <button
            style={{ background: "none", border: "none", cursor: "pointer", color: "inherit", padding: "0 0 0 4px", display: "flex", alignItems: "center", flexShrink: 0 }}
            onClick={(e) => { e.preventDefault(); setFile(null); }}
            title="Remove file"
          >
            <FiX size={13} />
          </button>
        </div>
      )}
    </div>
  );
}

export default FileUpload;