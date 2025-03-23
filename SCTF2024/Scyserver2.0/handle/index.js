var ritm = require('require-in-the-middle');
var patchChildProcess = require('./child_process');

new ritm.Hook(
    ['child_process'],
    function (module, name) {
        switch (name) {
            case 'child_process': {
                return patchChildProcess(module);
            }
        }
    }
);
