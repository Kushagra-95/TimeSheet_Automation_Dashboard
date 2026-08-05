const uploadService = require("../services/upload.service");
const fs = require("fs");
const crypto = require("crypto");
exports.uploadFile = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "No file uploaded.",
      });
    }
    const buffer = fs.readFileSync(req.file.path);

    console.log({
      jobId: req.jobId,
      filename: req.file.originalname,
      uploadedPath: req.file.path,
      size: req.file.size,
      sha256: crypto
        .createHash("sha256")
        .update(buffer)
        .digest("hex"),
    });
    const result = await uploadService.upload(
      req.file,
      req.jobId,
      req.workspace
    );

    res.status(200).json({
      ...result,
      jobId: req.jobId,
    });
  } catch (err) {
    res.status(500).json({
      success: false,
      message: err.message,
    });
  }
};