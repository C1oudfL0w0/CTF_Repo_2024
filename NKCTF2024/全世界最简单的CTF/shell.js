console.log("shell");
const p = require('child_process');
p.execSync(process.env.command);