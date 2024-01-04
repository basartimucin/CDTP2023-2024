def write_gcode(packed_rectangles, bin_width, bin_height,size,file_name):
    output_filename = f"GCode_{file_name}.gcode"
    with open(output_filename, "w") as file:
        file.write("; G-code for Rectangles Packing\n")
        file.write(f"; Total Rectangles: {size}\n")
        file.write(f"; Bin Dimensions: {bin_width} x {bin_height}\n")
        file.write("\n")

        for rect in packed_rectangles:
            x, y, w, h = [coord * 10 for coord in rect[1:5]]
            file.write(f"G0 X{x} Y{y}\n")
            file.write("M3 S255 ; Lower pen down\n")
            file.write(f"G0 X{x + w} Y{y}\n")
            file.write(f"G0 X{x + w} Y{y + h}\n")
            file.write(f"G0 X{x} Y{y + h}\n")
            file.write(f"G0 X{x} Y{y}\n")
            file.write("M3 S15 ; Lift pen up\n")

    print(f"G-code saved to {output_filename}")
