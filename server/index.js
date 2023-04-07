const express = require('express');
const cors = require('cors');
const path = require('path');
const { spawn } = require('child_process');
const app = express();
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

const isDev = process.env.NODE_ENV !== 'production';
const PORT = process.env.PORT || 5000;

if (!isDev && cluster.isMaster) {
  console.error(`Node cluster master ${process.pid} is running`);

  // Fork workers.
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.error(`Node cluster worker ${worker.process.pid} exited: code ${code}, signal ${signal}`);
  });

} else {
  app.use(cors());
  app.use(express.json());

  if (process.env.NODE_ENV === 'production') {
    app.use(express.static(path.join(__dirname, '../react-ui/build')));
  }
  app.use('/static', express.static(path.join(__dirname, 'static')));

  if (process.env.NODE_ENV === 'development') {
    app.use(cors());
  }

  app.post('/convert', (req, res) => {
    const md_content = req.body.md_content || '';

    // Use spawn instead of exec to pass the content via stdin
    const pythonProcess = spawn('python3', ['convert_to_html.py']);

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data;
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data;
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error('Error executing Python script:', stderr);
        res.status(500).json({ error: 'Error executing Python script', stderr });
      } else {
        const html_content = JSON.parse(stdout).html_content;
        res.json({ html_content });
      }
    });

    // Pass the content to the Python script via stdin
    pythonProcess.stdin.write(md_content);
    pythonProcess.stdin.end();
  });

  // All remaining requests return the React app, so it can handle routing.
  app.get('*', function(request, response) {
    response.sendFile(path.join(__dirname, '../react-ui/build', 'index.html'));
  });

  app.listen(PORT, () => {
    console.error(`Node ${isDev ? 'dev server' : 'cluster worker ' + process.pid}: listening on port ${PORT}`);
  });
}