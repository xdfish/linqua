const express = require('express')
const Vosk = require("@solyarisoftware/voskjs")
const multer = require('multer')
const cors = require('cors')
const nlp = require('compromise');

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'public/audio/')
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname)
    }
})

const app = express();
app.use(cors())

app.post('/solve-quiz', multer({ storage }).single('audio'), async (req, res) => {
    const result = await Vosk.transcriptFromFile(__dirname + "/public/audio/" + req.file.originalname, model);
    const fetchResult = await fetch(`http://localhost:8000/correct-sentence/${result.text}`).catch(() => {
        return null;
    });
    let correct_result = { correct_sentence: "Service is not running" };
    if (fetchResult) {
        correct_result = await fetchResult.json();
    }

    let points = 0;
    let score = 0;
    const keywords = req.body.keywords?.split(",");

    if (keywords?.length) {
        let doc = nlp(result.text);
        for (const keyword of keywords) {
            if (doc.has(keyword)) {
                points++;
            }
        }
        score = points / keywords.length * 10;
    }

    res.send({ text: result.text, ...correct_result, score })
})

const startApp = async () => {
    //vosk-model-small-en-us-0.15
    //vosk-model-en-us-0.42-gigaspeech
    model = await Vosk.loadModel(__dirname + "/public/models/vosk-model-small-en-us-0.15/");
    app.listen(3000);
    console.log("listen on port 3000")
}

startApp()