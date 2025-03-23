const express = require('express');
const fs = require('fs');
var nodeRsa = require('node-rsa');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const SECRET_KEY = crypto.randomBytes(16).toString('hex');
const path = require('path');
const zlib = require('zlib');
const mysql = require('mysql')
const handle = require('./handle');
const cp = require('child_process');
const cookieParser = require('cookie-parser');

const con = mysql.createConnection({
  host: 'localhost',
  user: 'ctf',
  password: 'ctf123123',
  port: '3306',
  database: 'sctf'
})
con.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err.message);
    setTimeout(con.connect(), 2000); // 2秒后重试连接
  } else {
    console.log('Connected to MySQL');
  }
});

const {response} = require("express");
const req = require("express/lib/request");

var key = new nodeRsa({ b: 1024 });
key.setOptions({ encryptionScheme: 'pkcs1' });

var publicPem = `-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5nJzSXtjxAB2tuz5WD9B//vLQ\nTfCUTc+AOwpNdBsOyoRcupuBmh8XSVnm5R4EXWS6crL5K3LZe5vO5YvmisqAq2IC\nXmWF4LwUIUfk4/2cQLNl+A0czlskBZvjQczOKXB+yvP4xMDXuc1hIujnqFlwOpGe\nI+Atul1rSE0APhHoPwIDAQAB\n-----END PUBLIC KEY-----`;
var privatePem = `-----BEGIN PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALmcnNJe2PEAHa27
PlYP0H/+8tBN8JRNz4A7Ck10Gw7KhFy6m4GaHxdJWeblHgRdZLpysvkrctl7m87l
i+aKyoCrYgJeZYXgvBQhR+Tj/ZxAs2X4DRzOWyQFm+NBzM4pcH7K8/jEwNe5zWEi
6OeoWXA6kZ4j4C26XWtITQA+Eeg/AgMBAAECgYA+eBhLsUJgckKK2y8StgXdXkgI
lYK31yxUIwrHoKEOrFg6AVAfIWj/ZF+Ol2Qv4eLp4Xqc4+OmkLSSwK0CLYoTiZFY
Jal64w9KFiPUo1S2E9abggQ4omohGDhXzXfY+H8HO4ZRr0TL4GG+Q2SphkNIDk61
khWQdvN1bL13YVOugQJBAP77jr5Y8oUkIsQG+eEPoaykhe0PPO408GFm56sVS8aT
6sk6I63Byk/DOp1MEBFlDGIUWPjbjzwgYouYTbwLwv8CQQC6WjLfpPLBWAZ4nE78
dfoDzqFcmUN8KevjJI9B/rV2I8M/4f/UOD8cPEg8kzur7fHga04YfipaxT3Am1kG
mhrBAkEA90J56ZvXkcS48d7R8a122jOwq3FbZKNxdwKTJRRBpw9JXllCv/xsc2ye
KmrYKgYTPAj/PlOrUmMVLMlEmFXPgQJBAK4V6yaf6iOSfuEXbHZOJBSAaJ+fkbqh
UvqrwaSuNIi72f+IubxgGxzed8EW7gysSWQT+i3JVvna/tg6h40yU0ECQQCe7l8l
zIdwm/xUWl1jLyYgogexnj3exMfQISW5442erOtJK8MFuUJNHFMsJWgMKOup+pOg
xu/vfQ0A1jHRNC7t
-----END PRIVATE KEY-----`;

const app = express();
app.use(bodyParser.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'static')));
app.use(cookieParser());

var Reportcache = {}

function verifyAdmin(req, res, next) {
  const token = req.cookies['auth_token'];

  if (!token) {
    return res.status(403).json({ message: 'No token provided' });
  }

  jwt.verify(token, SECRET_KEY, (err, decoded) => {
    if (err) {
      return res.status(403).json({ message: 'Failed to authenticate token' });
    }

    if (decoded.role !== 'admin') {
      return res.status(403).json({ message: 'Access denied. Admins only.' });
    }

    req.user = decoded;
    next();
  });
}

app.get('/hello', verifyAdmin ,(req, res)=> {
  res.send('<h1>Welcome Admin!!!</h1><br><img src="./1.jpeg" />');
});

app.get('/config', (req, res) => {
  res.json({
    publicKey: publicPem,
  });
});

var decrypt = function(body) {
  try {
    var pem = privatePem;
    var key = new nodeRsa(pem, {
      encryptionScheme: 'pkcs1',
      b: 1024
    });
    key.setOptions({ environment: "browser" });
    return key.decrypt(body, 'utf8');
  } catch (e) {
    console.error("decrypt error", e);
    return false;
  }
};

app.post('/login', (req, res) => {
  const encryptedPassword = req.body.password;
  const username = req.body.username;

  try {
    passwd = decrypt(encryptedPassword)
    if(username === 'admin') {
      const sql = `select (select password from user where username = 'admin') = '${passwd}';`
      con.query(sql, (err, rows) => {
        if (err) throw new Error(err.message);
        if (rows[0][Object.keys(rows[0])]) {
          const token = jwt.sign({username, role: username}, SECRET_KEY, {expiresIn: '1h'});
          res.cookie('auth_token', token, {secure: false});
          res.status(200).json({success: true, message: 'Login Successfully'});
        } else {
          res.status(200).json({success: false, message: 'Errow Password!'});
        }
      });
    } else {
      res.status(403).json({success: false, message: 'This Website Only Open for admin'});
    }
  } catch (error) {
    res.status(500).json({ success: false, message: 'Error decrypting password!' });
  }
});

app.get('/ExP0rtApi', verifyAdmin, (req, res) => {
  var rootpath = req.query.v;
  var file = req.query.f;

  file = file.replace(/\.\.\//g, '');
  rootpath = rootpath.replace(/\.\.\//g, '');

  if(rootpath === ''){
    if(file === ''){
      return res.status(500).send('try to find parameters HaHa');
    } else {
      rootpath = "static"
    }
  }

  const filePath = path.join(__dirname, rootpath + "/" + file);

  if (!fs.existsSync(filePath)) {
    return res.status(404).send('File not found');
  }
  fs.readFile(filePath, (err, fileData) => {
    if (err) {
      console.error('Error reading file:', err);
      return res.status(500).send('Error reading file');
    }

    zlib.gzip(fileData, (err, compressedData) => {
      if (err) {
        console.error('Error compressing file:', err);
        return res.status(500).send('Error compressing file');
      }
      const base64Data = compressedData.toString('base64');
      res.send(base64Data);
    });
  });
});

app.get("/report", verifyAdmin ,(req, res) => {
  res.sendFile(__dirname + "/static/report_noway_dirsearch.html");
});

app.post("/report", verifyAdmin ,(req, res) => {
  const {user, date, reportmessage} = req.body;
  if(Reportcache[user] === undefined) {
    Reportcache[user] = {};
  }
  Reportcache[user][date] = reportmessage
  res.status(200).send("<script>alert('Report Success');window.location.href='/report'</script>");
});

app.get('/countreport', (req, res) => {
  let count = 0;
  for (const user in Reportcache) {
    count += Object.keys(Reportcache[user]).length;
  }
  res.json({ count });
});

//查看当前运行用户
app.get("/VanZY_s_T3st", (req, res) => {
  var command = 'whoami';
  const cmd = cp.spawn(command ,[]);
  cmd.stdout.on('data', (data) => {
    res.status(200).end(data.toString());
  });
})

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});