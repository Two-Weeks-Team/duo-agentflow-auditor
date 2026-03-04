// Safe JavaScript — demonstrates secure patterns
"use strict";

const https = require("https");
const { execFile } = require("child_process");

const API_URL = "https://api.example.com/data";

function fetchData(endpoint) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, API_URL);
    https.get(url.toString(), (res) => {
      let data = "";
      res.on("data", (chunk) => { data += chunk; });
      res.on("end", () => resolve(JSON.parse(data)));
      res.on("error", reject);
    });
  });
}

function runCommand(command, args) {
  return new Promise((resolve, reject) => {
    execFile(command, args, (error, stdout) => {
      if (error) return reject(error);
      resolve(stdout.trim());
    });
  });
}

function getConfig() {
  const apiKey = process.env.API_KEY;
  if (!apiKey) throw new Error("API_KEY not set");
  return { apiKey, timeout: 30000 };
}

module.exports = { fetchData, runCommand, getConfig };
