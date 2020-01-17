...

; --- MODIFIED G-CODE 
G28 ; Home axis, move printhead away from camera 
M226 ; Initial pause until first layer is verified
; --- END MODIFIED G-CODE

G1 X94.595 Y136.025 E0.00936 ; perimeter
G1 X94.444 Y136.294 E0.00967 ; perimeter
..