const fs = require("fs");

exports.upload = async (file, jobId, workspace) => {
  if (!file) {
    throw new Error("No file uploaded.");
  }

  if (!fs.existsSync(file.path)) {
    throw new Error("File upload failed.");
  }

  return {
    success: true,
    message: "File uploaded successfully.",
    jobId,
    workspace,
    file: {
      originalName: file.originalname,
      fileName: file.filename,
      path: file.path,
      size: file.size,
      mimeType: file.mimetype,
    },
  };
};