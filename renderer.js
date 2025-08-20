async function sendTask(command) {
  const response = await fetch("http://127.0.0.1:5000/task", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command: command, context: "LGLGFG context" })
  });
  const data = await response.json();
  document.getElementById("output").innerText = JSON.stringify(data, null, 2);
}
