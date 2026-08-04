const multer = require("multer");
const path = require("path");
const fs = require("fs");
const { randomUUID } = require("crypto");
const { scheduleCleanup } = require("../utils/cleanup");


const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        try {
            const jobId = randomUUID();
            console.log(__dirname);
            
            const workspaceRoot = path.join(__dirname, "../../temp", jobId);
            const inputDir = path.join(workspaceRoot, "input");
            const outputDir = path.join(workspaceRoot, "output");

            // Create folders
            fs.mkdirSync(inputDir, { recursive: true });
            fs.mkdirSync(outputDir, { recursive: true });
            scheduleCleanup(workspaceRoot);
            // Store workspace details for later use
            req.jobId = jobId;
            req.workspace = {
                root: workspaceRoot,
                input: inputDir,
                output: outputDir,
            };

            cb(null, inputDir);
        } catch (err) {
            cb(err);
        }
    },

    filename: (req, file, cb) => {
        cb(null, file.originalname);
    },
});

module.exports = multer({
    storage,
});