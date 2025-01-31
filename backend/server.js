require('dotenv').config();
const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");
const axios = require("axios");

const app = express();
app.use(cors());
app.use(express.json());

// Scraper API Route
app.post("/search-flights", (req, res) => {
    const { from, to, date } = req.body;
    exec(`python scraper.py "${from}" "${to}" "${date}"`, (error, stdout, stderr) => {
        if (error) return res.status(500).json({ error: "Scraping failed" });
        res.json({ flights: JSON.parse(stdout) });
    });
});

// AI Chat Route (Using Ollama AI)
app.post("/chat", async (req, res) => {
    try {
        const response = await axios.post("http://localhost:11434/api/generate", {
            model: "llama3",
            prompt: req.body.message,
            stream: false
        });
        res.json({ reply: response.data.response });
    } catch (error) {
        res.status(500).json({ error: "Chat failed" });
    }
});

app.listen(3000, () => console.log("Backend running on port 3000"));