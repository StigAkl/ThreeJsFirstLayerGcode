

class App {
    constructor() {
        //Setup

        this.bedSize = {
            x: 250,
            y: 210
        }

        this.scene = new THREE.Scene(); 
        this.camera = new THREE.OrthographicCamera(window.innerWidth / - 6, window.innerWidth / 6,window.innerHeight / 6, window.innerHeight / - 6, -200,5000); 
        this.canvas = document.getElementById("canvas"); 
        
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true
        }); 


        this.renderer.shadowMap.enabled = true; 
        this.renderer.setClearColor(0xffffff,1.0);
        this.renderer.setSize(window.innerWidth,window.innerHeight); 
        document.body.appendChild(this.renderer.domElement); 

 
        var geometry = new THREE.BoxGeometry(10,10,10); 
        var material = new THREE.MeshBasicMaterial( {color: 0x000000, wireframe: true} );
        this.cube = new THREE.Mesh(geometry, material); 


        this.pgeometry = new THREE.PlaneGeometry( 500, 500, 32 );
        this.pmaterial = new THREE.MeshBasicMaterial( {color: 0x000000, side: THREE.DoubleSide} );
        this.plane = new THREE.Mesh( this.pgeometry, this.pmaterial );
        
        this.camera.position.set(0,0.3,1)
        
        this.camera.lookAt(this.cube.position)
        //this.scene.add(this.plane)
    
        //this.scene.add(cube); 

        var ambientLight = new THREE.AmbientLight(0x0c0c0c);
        this.scene.add(ambientLight);

        var spotLight = new THREE.SpotLight( 0xffffff );
        this.scene.add(spotLight);  

        document.getElementById("reset").addEventListener("click", () => {
            console.log("removing"); 
            while(this.scene.children.length > 0) {
                this.scene.remove(this.scene.children[0]); 
                this.fetchGcode(); 
            }
        });

        this.fetchGcode(); 
        this.render(); 
    }


    fetchGcode() {
        fetch("http://localhost:8080/api/getStrippedGcode").then((res)=>{
            return res.json(); 
        }).then((data) => {
            this.drawPolygons(data);
            this.setSlider(data);  
        })
    }

    setSlider(data) {
        //numLayers = data.numLayers;
        //document.getElementById("setLayer").max = data.numLayers; 
    }

     drawGcode(gcode) {

        var material = new THREE.LineBasicMaterial( {
            color: 0x0000ff, 
            linewidth: 1000
        } );        
        var geometry = new THREE.Geometry(); 

        for(let i = 0; i < 10; i++) {
            if(gcode.numPoints > 0) {
                const points = gcode.points; 

                points.forEach(p => {
                    geometry.vertices.push(new THREE.Vector3(p.x, i, p.y)); 
                }); 
            }
        }

        var line = new THREE.Line(geometry, material); 


        var middle = this.getCenter(line); 
        line.position.set(-middle.x, 0, -middle.z); 
        this.scene.add(line);

    }
    
    drawPolygons(gcode) {

        let polygons = gcode.polygons; 

        let numPoints = 0; 
        for(let j = 0; j < 10; j++) {
            for(let i = 0; i < polygons.length; i++) {

                //Simulate errors
                //if(i % 10 !== 0) {
                if(true) {
                    let points = polygons[i];

                    var material = new THREE.LineBasicMaterial( {
                        color: 0x0000ff, 
                        linewidth: 1000
                    } );


                    var geometry = new THREE.Geometry(); 

                    let t = 0; 
                    points.forEach(p => {
                        numPoints++; 
                        geometry.vertices.push(new THREE.Vector3(p.point.x-(this.bedSize.x/2), (j/2), p.point.y-(this.bedSize.y/2))); 
                    }); 

                    var line = new THREE.Line(geometry, material); 

                    this.scene.add(line);
                }
            }
        }

    console.log(numPoints); 


    }

    getCenter(mesh) {
        var middle = new THREE.Vector3();
        var geometry = mesh.geometry;

        geometry.computeBoundingBox();
        middle.x = (geometry.boundingBox.max.x + geometry.boundingBox.min.x) / 2;
        middle.y = (geometry.boundingBox.max.y + geometry.boundingBox.min.y) / 2;
        middle.z = (geometry.boundingBox.max.z + geometry.boundingBox.min.z) / 2;    
        mesh.localToWorld( middle );
        
        return middle; 
    }

    render() {
        this.camera.lookAt(this.cube.position)
        this.renderer.render(this.scene, this.camera); 
        window.requestAnimationFrame(this.render.bind(this)); 
    }
}

var app = new App(); 