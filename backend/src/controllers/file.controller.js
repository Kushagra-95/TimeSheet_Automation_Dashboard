const fs = require("fs/promises");
const path = require("path");

const fileService = require("../services/file.service");

exports.downloadFile = async (req, res) => {
  try {
    const { filename } = req.params;
    const { jobId } = req.query;

    if (!jobId) {
      return res.status(400).json({
        success: false,
        message: "jobId is required",
      });
    }

    const filePath = fileService.getFilePath(jobId, filename);

    res.download(filePath, filename, async (err) => {
      if (err) {
        console.error(err);
      }

      // Cleanup can be added here later if desired
      // await fs.rm(
      //   path.join(__dirname, "../../temp", jobId),
      //   { recursive: true, force: true }
      // );
    });
  } catch (error) {
    res.status(404).json({
      success: false,
      message: error.message,
    });
  }
};