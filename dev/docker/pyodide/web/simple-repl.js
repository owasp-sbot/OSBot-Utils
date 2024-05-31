// This works ok (on initial osbot-commands)
//
// todo: figure out how what is the prob with GET
// await micropip.install("ssl")
// from osbot_utils.utils.Http import *
// GET('https://www.google.com')   # didn't work
// GET('http://localhost:8080/')    # also din't work, give urllib.error.URLError: <urlopen error [Errno 26] Operation in progress>

// since this works
// micropip.install("requests")
// import requests                     # failed with ImportError: cannot import name 'JsArray' from 'pyodide.ffi'
// requests.get('http://localhost:8080')
// requests.get('https://www.google.com') # this fails with  HTTPException("Failed to execute 'send' on 'XMLHttpRequest': Fail
// ed to load 'https://www.google.com/'."))

// try this on this ui
// await micropip.install("requests")
// import requests
// requests.get('http://localhost:8080')

let pyodideReady = false;

async function loadPyodideAndPackages() {
    let pyodide = await loadPyodide();
    await pyodide.loadPackage(['micropip']);
    await pyodide.runPythonAsync(`
        import micropip
        await micropip.install('osbot-utils')
    `);
    pyodideReady = true;
    return pyodide;
}

let pyodideInstance = loadPyodideAndPackages();

async function runCode() {
    if (!pyodideReady) {
        document.getElementById('output').innerText = 'Pyodide is still loading. Please wait...';
        return;
    }

    let code = document.getElementById('code-input').value;
    try {
        let pyodide = await pyodideInstance;
        let output = await pyodide.runPythonAsync(code);
        document.getElementById('output').innerText = output;
    } catch (err) {
        document.getElementById('output').innerText = err;
    }
}
