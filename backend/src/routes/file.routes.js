const express = require("express");
const router = express.Router();

const fileController = require("../controllers/file.controller");


router.get("/download/:filename", fileController.downloadFile);

module.exports = router;