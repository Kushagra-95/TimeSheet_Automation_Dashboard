const path = require("path");
const fs = require("fs");
const archiver = require("archiver");

exports.downloadFolder = (jobId, folderName, res) => {

  const folderPath = path.join(
    __dirname,
    "../../temp",
    jobId,
    "output",
    folderName
  );

  if (!fs.existsSync(folderPath)) {
    throw new Error("Folder not found.");
  }

  if (!fs.statSync(folderPath).isDirectory()) {
    throw new Error("Requested path is not a folder.");
  }

  res.attachment(`${folderName}.zip`);

  const archive = archiver("zip", {
    zlib: { level: 9 },
  });

  archive.on("error", (err) => {
    throw err;
  });

  archive.pipe(res);

  archive.directory(folderPath, false);

  archive.finalize();
};