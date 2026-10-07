# Timesheet Automation Web Application

A full-stack web application designed to automate the processing, repairing, and generation of employee timesheets from raw data exports (such as SAP-generated Excel files).

---

## 📌 Architecture Overview

The application is structured into three main layers:

- **Frontend (`frontend2/`)**: Modern React application built with Vite, providing a dashboard to upload files, monitor workflow execution progress, inspect live logs, and download generated timesheet outputs.
- **Backend (`backend/`)**: Node.js & Express REST API managing file uploads, workspace job sessions, orchestration of Python automation scripts, and file/folder downloads.
- **Python Automation Engine (`python/`)**: Python data-processing scripts using `pandas` and `openpyxl` that repair corrupted/unsupported SAP XML elements and generate formatted individual and consolidated timesheets.

---

## 📁 Project Structure

```text
Timesheet_webapp/
├── backend/
│   ├── src/
│   │   ├── config/              # Workflow definitions (workflow.json)
│   │   ├── controllers/         # Express controllers (upload, workflow, file, folder)
│   │   ├── middleware/          # Multer upload & session middleware
│   │   ├── routes/              # API endpoints routing
│   │   ├── services/            # Business logic & Python child process execution
│   │   ├── app.js               # Express application configuration
│   │   └── server.js            # Server entry point (Port 8000)
│   └── package.json
│
├── frontend2/
│   ├── src/
│   │   ├── components/          # Dashboard cards, file upload, console, output view
│   │   ├── pages/               # Dashboard view
│   │   ├── services/            # Axios API client (workflowApi.js)
│   │   ├── App.jsx              # Main React component
│   │   └── main.jsx             # React entry point
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── python/
│   ├── Generate_Timesheets.py   # Excel repair, parsing, and timesheet generation
│   └── requirements.txt         # Python dependencies (pandas, openpyxl)
│
└── README.md
```

---

## ✨ Features

- **Drag-and-Drop File Upload**: Upload raw timesheet files (.xlsx) through a clean, intuitive dashboard.
- **Session Isolation**: Each upload generates a unique `jobId` workspace under `backend/temp/<jobId>` with isolated `input` and `output` directories.
- **Automated SAP Excel Repair**: Automatically fixes corrupted `<fill/>` elements in SAP-exported Excel files that cause standard spreadsheet engines to crash.
- **Real-Time Job Monitoring**: Live status indicator, runtime duration tracker, and terminal-style console logging.
- **Single & Bulk Downloads**: Download individual Excel output files or entire output folders as compressed `.zip` archives.

---

## 🛠️ Prerequisites

Ensure you have the following installed on your machine:

- **Node.js** (v18.x or later) & **npm**
- **Python** (v3.8 or later) with `pip` added to system PATH

---

## 🚀 Getting Started

### 1. Python Environment Setup

Navigate to the `python/` directory and install the required Python packages:

```bash
cd python
pip install -r requirements.txt
cd ..
```

*Required libraries:*
- `pandas`
- `openpyxl`

---

### 2. Backend Setup

Navigate to the `backend/` directory, install dependencies, and start the API server:

```bash
cd backend
npm install
npm start
```

The backend server runs at:
`http://localhost:8000`

---

### 3. Frontend Setup

In a new terminal window, navigate to the `frontend2/` directory, install dependencies, and start the Vite development server:

```bash
cd frontend2
npm install
npm run dev
```

The frontend application will be accessible at:
`http://localhost:5173` (or the port specified by Vite)

---

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/upload` | Uploads the source `.xlsx` file and initializes workspace (`jobId`). |
| `POST` | `/api/workflow/run` | Triggers Python workflow execution for the specified `jobId`. |
| `GET` | `/api/files/download/:filename?jobId=:id` | Downloads a specific generated output file. |
| `GET` | `/api/folders/download/:folderName?jobId=:id` | Compresses and streams a directory of generated timesheets as a `.zip`. |

---

## ⚙️ Workflow Configuration

The execution pipeline is defined in `backend/src/config/workflow.json`:

```json
{
  "steps": [
    {
      "script": "Generate_Timesheets.py",
      "enabled": true
    }
  ]
}
```

Additional Python processing steps can be appended to `steps` to extend or customize the pipeline.

