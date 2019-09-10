const fs = require("fs"); 
const pathToGcode = "./app/gcode/"; 
const gcode = require("./constants/gcode"); 
const fileName = "octopus.gcode"; 
getLayerHeight = () => {

    let layerHeight = undefined; 
    let layerHeightFound = false; 
    fs.readFileSync(pathToGcode + fileName, "utf-8").split(/\r?\n/).forEach(line=>{
        if(line.includes("first_layer_height")) {
            if(!layerHeightFound) {
                lineSplit = line.split(" = "); 
                layerHeight = parseFloat(lineSplit[lineSplit.length-1]);
                layerHeightFound = true; 
            }
        }
    }) 

    return layerHeight; 

}

exports.gcodeController = (req, res) => {

    const linearPoints = []; 
    const perimeterPoints = [];
    const infillPoints = []; 

    const layerHeight = getLayerHeight(); 
    
    let isOnFirstLayer = true; 

    fs.readFileSync(pathToGcode + fileName, 'utf-8').split(/\r?\n/).forEach(function(line){
        const splitCode = line.split(" "); 
        const splitComment = line.split(" ; "); 

        if(isOnFirstLayer) {
            if(splitComment.length > 1 && splitComment[1].includes("restore layer Z")) {
                splitLayerRestoreLine = line.split(" "); 
                console.log(splitLayerRestoreLine); 
                if(splitLayerRestoreLine[1].startsWith("Z")) {
                    let currentLayerHeight = parseFloat(splitLayerRestoreLine[1].substring(1, splitLayerRestoreLine[1].length)); 

                    console.log(currentLayerHeight); 
                    if(currentLayerHeight > layerHeight) {
                        isOnFirstLayer = false; 
                    }
                }
            }
                if(splitCode.length && splitCode[0] === gcode.LinearMovement) {
                    if(splitCode[1].startsWith("X") && splitCode[2].startsWith("Y") && splitCode[3].startsWith("E")) {

                        var positiveExtrusion = parseFloat(splitCode[3].substring(1, splitCode[3].length)) > 0 ? true : false;

                        if(positiveExtrusion) {
                            switch(splitCode[splitCode.length-1]) {

                                case gcode.Perimeter: 
                                    perimeterPoints.push({
                                        x: splitCode[1].substring(1, splitCode[1].length),
                                        y: splitCode[2].substring(1, splitCode[2].length) 
                                    })
                                break;

                                case gcode.Infill: 
                                    infillPoints.push({
                                        x: splitCode[1].substring(1, splitCode[1].length),
                                        y: splitCode[2].substring(1, splitCode[2].length) 
                                    })
                            }

                            linearPoints.push({
                                x: splitCode[1].substring(1, splitCode[1].length),
                                y: splitCode[2].substring(1, splitCode[2].length)
                            })
                        }
                    }
                }
                
        }
      })

      res.json({
          numPoints: perimeterPoints.length,
          points: perimeterPoints
      }); 
}