const express = require('express');
const app = express();
const port = process.env.PORT || 8080;
const { gcodeController } = require("./controllers/stripGcodeControllerNoComment");  

app.listen(port, (req) => {
    console.log("Listening on port " + port); 
})

app.get("/api/getStrippedGcode", gcodeController); 

app.use(express.static('app')); 