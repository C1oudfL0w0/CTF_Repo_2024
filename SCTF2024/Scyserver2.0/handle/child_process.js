function patchChildProcess(cp) {

    cp.execFile = new Proxy(cp.execFile, { apply: patchOptions(true) });
    cp.fork = new Proxy(cp.fork, { apply: patchOptions(true) });
    cp.spawn = new Proxy(cp.spawn, { apply: patchOptions(true) });
    cp.execFileSync = new Proxy(cp.execFileSync, { apply: patchOptions(true) });
    cp.execSync = new Proxy(cp.execSync, { apply: patchOptions() });
    cp.spawnSync = new Proxy(cp.spawnSync, { apply: patchOptions(true) });

    return cp;
}

function patchOptions(hasArgs) {
    return function apply(target, thisArg, args) {
        var pos = 1;
        if (pos === args.length) {
            args[pos] = prototypelessSpawnOpts();
        } else if (pos < args.length) {
            if (hasArgs && (Array.isArray(args[pos]) || args[pos] == null)) {
                pos++;
            }
            if (typeof args[pos] === 'object' && args[pos] !== null) {
                args[pos] = prototypelessSpawnOpts(args[pos]);
            } else if (args[pos] == null) {
                args[pos] = prototypelessSpawnOpts();
            } else if (typeof args[pos] === 'function') {
                args.splice(pos, 0, prototypelessSpawnOpts());
            }
        }

        return target.apply(thisArg, args);
    };
}

function prototypelessSpawnOpts(obj) {
    var prototypelessObj = Object.assign(Object.create(null), obj);
    prototypelessObj.env = Object.assign(Object.create(null), prototypelessObj.env || process.env);
    return prototypelessObj;
}

module.exports = patchChildProcess;