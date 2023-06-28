const csvtojson = require('csvtojson');
const mongoose = require('mongoose');

const url = "Enter your mongodb url here";

const importCsv = async () => {
    // Connect to mongodb databaase
    await mongoose.connect(url, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    });
    const WordInfo = mongoose.model('WordInfo', {
        Word: String,
        FREQcount: String,
        CDcount: String,
        FREQlow: String,
        Cdlow: String,
        SUBTLWF: String,
        Lg10WF: String,
        SUBTLCD: String,
        Lg10CD: String,
        Dom_PoS_SUBTLEX: String,
        Freq_dom_PoS_SUBTLEX: String,
        Percentage_dom_PoS: String,
        All_PoS_SUBTLEX: String,
        All_freqs_SUBTLEX: String
    })
    // Read file
    const filePath = __dirname + '/SUBTLEX-US frequency list with PoS information.csv';
    const csvData = await csvtojson().fromFile(filePath);

    // Insert into database
    await WordInfo.insertMany(csvData);
    const documentsLength = await WordInfo.count();
    console.log(`Imported ${documentsLength} words.`);
}

importCsv()