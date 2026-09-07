const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const baseUrl = process.env.CIRCUITSENSE_URL || "http://localhost:8501";
const outputDir = path.join(__dirname, "..", "assets", "screenshots");

const pages = [
  ["Overview", "overview.png"],
  ["Analysis: Voltage Divider", "voltage-divider.png"],
  ["Analysis: Network Solver", "network-solver.png"],
  ["Fault & Diagnostics", "fault-diagnostics.png"],
  ["Monte Carlo Analysis", "monte-carlo.png"],
];

async function main() {
  fs.mkdirSync(outputDir, { recursive: true });
  const browser = await chromium.launch({ channel: "msedge", headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });

  for (const [label, filename] of pages) {
    const url = `${baseUrl}/?page=${encodeURIComponent(label)}`;
    await page.goto(url, { waitUntil: "networkidle" });
    await page.waitForTimeout(1500);
    await page.screenshot({
      path: path.join(outputDir, filename),
      fullPage: true,
    });
    console.log(`Captured ${filename}`);
  }

  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
