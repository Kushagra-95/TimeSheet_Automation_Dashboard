import { FiUpload, FiFileText } from "react-icons/fi";
import "../App.css";
function FileUpload({ file, setFile }) {
  return (
    <div className="upload-card">
      <label className="upload-label">
        Upload Timesheet
      </label>

      <label className="upload-box">
        <FiUpload className="upload-icon" />

        <div>
          <p className="upload-title">Click to upload Excel file</p>
          <span className="upload-subtitle">
            Supported formats: .xlsx, .xls
          </span>
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
        </div>
      )}
    </div>
  );
}

export default FileUpload;