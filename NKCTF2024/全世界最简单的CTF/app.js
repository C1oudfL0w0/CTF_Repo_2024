const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const fs = require("fs");
const path = require('path');
const vm = require("vm");

app
.use(bodyParser.json())
.set('views', path.join(__dirname, 'views'))
.use(express.static(path.join(__dirname, '/public')))

app.get('/', function (req, res){
    res.sendFile(__dirname + '/public/home.html');
})


function waf(code) {
    let pattern = /(process|\[.*?\]|exec|spawn|Buffer|\\|\+|concat|eval|Function)/g;
    if(code.match(pattern)){
        throw new Error("what can I say? hacker out!!");
    }
}

app.post('/', function (req, res){
        let code = req.body.code;
        let sandbox = Object.create(null);
        let context = vm.createContext(sandbox);
        try {
            waf(code)
            let result = vm.runInContext(code, context);
            console.log(result);
        } catch (e){
            console.log(e.message);
            require('./hack');
        }
})

app.get('/secret', function (req, res){
    if(process.__filename == null) {
        let content = fs.readFileSync(__filename, "utf-8");
        return res.send(content);
    } else {
        let content = fs.readFileSync(process.__filename, "utf-8");
        return res.send(content);
    }
})


app.listen(3000, ()=>{
    console.log("listen on 3000");
})