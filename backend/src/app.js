const express=require("express")
const cors=require("cors")
const workflowRoutes=require("./routes/workflow.routes")
const fileRoutes=require("./routes/file.routes")
const folderRoutes = require("./routes/folder.routes");
const uploadRoutes=require("./routes/upload.routes")

const app=express();

app.use(cors());
app.use(express.json());

app.use("/api/workflow",workflowRoutes)
app.use("/api/files", fileRoutes);
app.use("/api/folders", folderRoutes);
app.use("/api/upload",uploadRoutes)

module.exports=app;