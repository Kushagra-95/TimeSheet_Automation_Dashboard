const fs = require("fs/promises");

function scheduleCleanup(workspacePath, delay = 1 * 60 * 1000) {
  setTimeout(async () => {
    try {
      await fs.rm(workspacePath, {
        recursive: true,
        force: true,
      });

      console.log(`Workspace deleted: ${workspacePath}`);
    } catch (err) {
      console.error(`Cleanup failed: ${workspacePath}`, err);
    }
  }, delay);
}

module.exports = {
  scheduleCleanup,
};