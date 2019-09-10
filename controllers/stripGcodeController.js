const fs = require("fs"); 
const pathToGcode = "./app/gcode/"; 
const gcode = require("./constants/gcode"); 

exports.gcodeController = (req, res) => {

    const points = []; 

    fs.readFileSync(pathToGcode + "square.gcode", 'utf-8').split(/\r?\n/).forEach(function(line){
        const split = line.split(" "); 
        console.log(line); 
        if(split[0] === gcode.LinearMovement) {
            
            split[1].startsWith("X") && split[2].startsWith("Y") 
            ? 
            points.push({
                x: split[1].substring(1, split[1].length),
                y: split[2].substring(1, split[2].length)
            })
            : 
            console.log("Undefined"); 
        }
      }) 
      res.json({
          numPoints: points.length,
          points: points
      }); 
}