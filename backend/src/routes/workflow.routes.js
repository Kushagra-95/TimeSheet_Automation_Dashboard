const express=require("express")

const controller=require("../controllers/workflow.controller")
const router =express.Router();

router.post("/run",controller.runWorkflow);

module.exports=router;