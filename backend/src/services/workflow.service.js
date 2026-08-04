const fs = require("fs");
const fsp = require("fs/promises");
const path = require("path");

const pythonService = require("./python.service");

exports.run = async (workspace) => {
  const workflowPath = path.join(
    __dirname,
    "../config/workflow.json"
  );

  const workflow = JSON.parse(
    await fsp.readFile(workflowPath, "utf8")
  );

  const results = [];

  for (const step of workflow.steps) {
    if (!step.enabled) continue;

    let output;

    // switch (step.script) {
    //   case "Fetch_Details.py":
    //     output = await pythonService.execute(step.script, [
    //       workspace.input,
    //       workspace.output,
    //     ]);
    //     break;

    //   case "split_excel.py":
    //     output = await pythonService.execute(step.script, [
    //       path.join(workspace.output, "master.xlsx"),
    //       path.join(workspace.output, "output_sheets"),
    //     ]);
    //     break;

    //   default:
    //     output = await pythonService.execute(step.script);
    // }
    output = await pythonService.execute(step.script, [
      workspace.input,
      workspace.output,
  ]);

    results.push({
      script: step.script,
      output,
    });
  }

  const items = [];

  if (fs.existsSync(workspace.output)) {
    const entries = await fsp.readdir(workspace.output);

    for (const entry of entries) {
      if (entry.endsWith(".py")) continue;

      const entryPath = path.join(workspace.output, entry);
      const stats = await fsp.stat(entryPath);

      items.push({
        name: entry,
        type: stats.isDirectory() ? "folder" : "file",
      });
    }
  }

  return {
    success: true,
    results,
    items,
  };
};