const fs = require("fs"); 
const pathToGcode = "./app/gcode/"; 
const gcode = require("./constants/gcode"); 
const fileName = "standrobot.gcode"; 

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

getConstantLayerHeight = () => {
    
    let layerHeight = undefined; 
    let layerHeightFound = false; 

    fs.readFileSync(pathToGcode + fileName, "utf-8").split(/\r?\n/).forEach(line=>{
        if(line.includes("layer_height")) {
            if(!layerHeightFound) {
                lineSplit = line.split(" = "); 

                if(lineSplit[0] === "; layer_height") {
                    layerHeight = parseFloat(lineSplit[lineSplit.length-1]);
                    layerHeightFound = true; 
                }
            }
        }
    }) 

    return layerHeight; 
}

const numLayers = getNumLayers = () => {
    let num_layers = -1; 
    fs.readFileSync(pathToGcode + fileName, "utf-8").split(/\r?\n/).forEach(line=>{
        if(line.includes("AFTER_LAYER_CHANGE")) {
           num_layers+=1; 
        }
    }) 

    return num_layers; 
}

exports.gcodeController = (req, res) => {

    const perimeterPoints = [];

    const layerHeight = getLayerHeight(); 

    const constantLayerHeight = getConstantLayerHeight(); 
    
    const numLayers = getNumLayers(); 

    const layerNum = 1;
    
    let layer = layerNum*layerHeight; 
    
    let isOnCorrectLayer = false; 
    let lastFeedrateChange = false; 

    let afterLayerChange = false; 

    let currentLayer = getLayerHeight(); 

    fs.readFileSync(pathToGcode + fileName, 'utf-8').split(/\r?\n/).forEach(function(line){
        const splitCode = line.split(" "); 

        
        if(afterLayerChange) {
            currentLayer = parseFloat(line.split(";")[1]); 
            afterLayerChange = false; 
        }

        if(currentLayer > layer) {
            isOnCorrectLayer = false;
        }

        if(currentLayer == layer) {
            isOnCorrectLayer = true; 
        }

        if(line === ";AFTER_LAYER_CHANGE") {
            afterLayerChange = true; 
        } 

        if(isOnCorrectLayer) {
             
            if(splitCode.length > 1 && splitCode[1].includes(gcode.FeedRate)) {
                lastFeedrateChange = true; 
            }
                if(splitCode.length && splitCode[0] === gcode.LinearMovement) {
                    if(splitCode.length >= 4 && splitCode[1].startsWith("X") && splitCode[2].startsWith("Y") && splitCode[3].startsWith("E")) {

                        var positiveExtrusion = parseFloat(splitCode[3].substring(1, splitCode[3].length)) > 0 ? true : false;

                        if(positiveExtrusion) {
                            perimeterPoints.push({
                                x: splitCode[1].substring(1, splitCode[1].length),
                                y: splitCode[2].substring(1, splitCode[2].length),
                                newPolygon: lastFeedrateChange,
                            })
                        }
                    }
                }
                
        }
      });   

      let polygons = [[]];
      let polygonIndex = 0; 

      for(let i = 0; i < perimeterPoints.length; i++) {

        if(i > 0 && perimeterPoints[i].newPolygon) {
            polygonIndex++; 
            polygons[polygonIndex] = new Array(); 
        }
          polygons[polygonIndex].push({
              polygon: polygonIndex,
              point: perimeterPoints[i]});
      }

      res.json({
        numLayers: numLayers,
          numPolygons: polygons.length,
          polygons: polygons
      })

    //   res.json({
    //       numPoints: perimeterPoints.length,
    //       points: perimeterPoints
    //   }); 
}