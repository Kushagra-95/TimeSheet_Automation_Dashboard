const path = require("path");
const workflowService = require("../services/workflow.service");

exports.runWorkflow = async (req, res) => {
  try {
    const { jobId } = req.body;

    if (!jobId) {
      return res.status(400).json({
        success: false,
        message: "jobId is required.",
      });
    }

    const workspace = {
      root: path.join(__dirname, "../../temp", jobId),
      input: path.join(__dirname, "../../temp", jobId, "input"),
      output: path.join(__dirname, "../../temp", jobId, "output"),
    };

    const result = await workflowService.run(workspace);
    console.log(result);
    res.status(200).json(result);
  } catch (error) {
    res.status(500).json({
      success: false,
      message: error.message,
    });
  }
};