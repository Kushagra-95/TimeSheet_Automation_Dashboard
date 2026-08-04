const express = require("express");
const router = express.Router();

const upload= require("../middleware/upload.middleware")
const uploadController =require("../controllers/upload.controller")


router.post("/",upload.single("file"),uploadController.uploadFile);

module.exports=router;