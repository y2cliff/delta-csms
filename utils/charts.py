months = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]
                 #Blue      Yellow     Red        Green      Peach      Rose       Pink
colorPalette = ["#4285f4", "#fbbc04", "#ea4335", "#34a853", "#fab1a0", "#ff7675", "#fd79a8"]
                  #Gold      Violet     Blue       Green      Brown      Maroon     BlueGreen  DarkGray   Brown
colorPalette2 = ["#ffb900", "#5a3286", "#0a53a8", "#11734b", "#753800", "#b10202", "#215a6c", "#3d3d3d", "#473822" ]
colorPrimary, colorSuccess, colorDanger = "#79aec8", colorPalette[0], colorPalette[2]


def get_year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict


def generate_color_palette(amount):
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0

    return palette
