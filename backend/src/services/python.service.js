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
            console.log("Exit Code:", code);
            console.log("Stdout:", output);
            console.log("Stderr:", error);
            if (code !== 0) {
                reject(new Error(error || `Python exited with code ${code}`));
            } else {
                resolve(output);
            }
        });

        python.on("error", (err) => {
            console.error("Spawn Error:", err);
            reject(err);
        });
    });
};