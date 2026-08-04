const path = require("path");
const fs = require("fs");

exports.getFilePath = (jobId, filename) => {
  const filePath = path.join(
    __dirname,
    "../../temp",
    jobId,
    "output",
    filename
  );

  if (!fs.existsSync(filePath)) {
    throw new Error("File not found");
  }

  return filePath;
};