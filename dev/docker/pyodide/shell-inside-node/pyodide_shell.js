const fs = require('fs');
const {loadPyodide} = require('pyodide');

// Function to load Pyodide and run Python code
async function main() {
    let pyodide = await loadPyodide();

    // Install osbot-utils using micropip
    await pyodide.loadPackage('micropip');
    await pyodide.runPythonAsync(`
        import micropip
        await micropip.install('osbot-utils')
    `);

    // Function to evaluate Python code
    const evaluatePython = async (code) => {
        try {
            let result = await pyodide.runPythonAsync(code);
            console.log(result);
        } catch (err) {
            console.error(err);
        }
    };

    // Read commands from stdin
    process.stdin.setEncoding('utf8');
    console.log('Pyodide Shell with osbot-utils. Type your Python code and press Enter.');
    process.stdin.on('data', async (data) => {
        await evaluatePython(data);
    });
}

// Start the main function
main();
