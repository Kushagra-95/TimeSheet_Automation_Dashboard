const path = require("path");
const { spawn } = require("child_process");

exports.execute = (scriptName, args = []) => {
    return new Promise((resolve, reject) => {

        const scriptPath = path.join(
            __dirname,
            "../../../python",
            scriptName
        );

        const python = spawn("python", [
            scriptPath,
            ...args
        ]);

        let output = "";
        let error = "";

        python.stdout.on("data", (data) => {
            output += data.toString();
        });

        python.stderr.on("data", (data) => {
            error += data.toString();
        });

        python.on("close", (code) => {
            if (code !== 0) {
                reject(new Error(error || `Python exited with code ${code}`));
            } else {
                resolve(output);
            }
        });

        python.on("error", reject);
    });
};