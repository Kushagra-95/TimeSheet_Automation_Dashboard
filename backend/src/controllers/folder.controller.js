const folderService = require("../services/folder.service");

exports.downloadFolder = (req, res) => {
  try {
    const { folderName } = req.params;
    const { jobId } = req.query;

    if (!jobId) {
      return res.status(400).json({
        success: false,
        message: "jobId is required",
      });
    }

    folderService.downloadFolder(jobId, folderName, res);
  } catch (err) {
    res.status(404).json({
      success: false,
      message: err.message,
    });
  }
};