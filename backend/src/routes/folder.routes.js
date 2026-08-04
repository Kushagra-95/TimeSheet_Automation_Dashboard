const express = require("express");
const router = express.Router();

const folderController = require("../controllers/folder.controller");

router.get(
  "/download/:folderName",
  folderController.downloadFolder
);

module.exports = router;