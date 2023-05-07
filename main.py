from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageEditor:
    def __init__(self, master):
        self.master = master
        master.title("Image Editor")
        master.geometry("800x600")

        self.button_width = 18

        # Create buttons
        self.select_button = Button(master, text="Wybierz obraz", command=self.select_image, width=self.button_width)
        self.brightness_button = Button(master, text="Rozjaśnianie", command=self.brightness, width=self.button_width)
        self.darkness_button = Button(master, text="Zaciemnienie", command=self.darkness, width=self.button_width)
        self.negative_button = Button(master, text="Negatyw", command=self.negative, width=self.button_width)
        self.save_button = Button(master, text="Zapisz", command=self.save_image, width=self.button_width)
        self.cancel_button = Button(master, text="Cofnij zmiany", command=self.cancel_changes, width=self.button_width)
        self.overlay_button = Button(master, text="Nałożyć", command=self.overlay, width=self.button_width)
        self.subtract_button = Button(master, text="Odjąć", command=self.subtract, width=self.button_width)
        self.roberts_button = Button(master, text="Filtr Robertsa", command=self.roberts, width=self.button_width)



        # Set button positions
        self.select_button.grid(row=0, column=0, padx=10, pady=15)
        self.brightness_button.grid(row=1, column=0, padx=10, pady=15)
        self.darkness_button.grid(row=2, column=0, padx=10, pady=15)
        self.negative_button.grid(row=3, column=0, padx=10, pady=15)
        self.overlay_button.grid(row=4, column=0, padx=10, pady=15)

        self.save_button.grid(row=8, column=0, padx=10, pady=15)
        self.cancel_button.grid(row=7, column=0, padx=10, pady=15)
        self.subtract_button.grid(row=5, column=0, padx=10, pady=15)
        self.roberts_button.grid(row=6, column=0, padx=10, pady=15)




        self.canvas = Canvas(master, width=600, height=400)
        self.canvas.grid(row=0, column=1, rowspan=6, padx=10, pady=10)


        self.image = None
        self.original_image = None
        self.edited_image = None

    def select_image(self):

        file_path = filedialog.askopenfilename()
        if file_path:

            self.image = Image.open(file_path)
            self.original_image = self.image.copy()
            self.edited_image = self.image.copy()
            self.display_image()

    def display_image(self):

        self.image = self.edited_image.resize((300, 400))

        photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=photo, anchor=NW)
        self.canvas.image = photo

    def brightness(self):

        pixels = self.edited_image.load()
        for i in range(self.edited_image.size[0]):
            for j in range(self.edited_image.size[1]):
                r, g, b = pixels[i, j]
                r = min(r + 50, 255)
                g = min(g + 50, 255)
                b = min(b + 50, 255)
                pixels[i, j] = (r, g, b)
        self.display_image()

    def darkness(self):

        pixels = self.edited_image.load()
        for i in range(self.edited_image.size[0]):
            for j in range(self.edited_image.size[1]):
                r, g, b = pixels[i, j]
                r = max(r - 50, 0)
                g = max(g - 50, 0)
                b = max(b - 50, 0)
                pixels[i, j] = (r, g, b)
        self.display_image()

    def negative(self):

        pixels = self.edited_image.load()
        for i in range(self.edited_image.size[0]):
            for j in range(self.edited_image.size[1]):
                r, g, b = pixels[i, j]
                pixels[i, j] = (255 - r, 255 - g, 255 - b)
        self.display_image()

    def overlay(self):

        file_path = filedialog.askopenfilename()
        if file_path:

            overlay_image = Image.open(file_path)
            overlay_image = overlay_image.resize(self.edited_image.size)


            pixels1 = self.edited_image.load()
            pixels2 = overlay_image.load()
            for i in range(self.edited_image.size[0]):
                for j in range(self.edited_image.size[1]):
                    r1, g1, b1 = pixels1[i, j]
                    r2, g2, b2 = pixels2[i, j]
                    r = int((r1 + r2) / 2)
                    g = int((g1 + g2) / 2)
                    b = int((b1 + b2) / 2)
                    pixels1[i, j] = (r, g, b)

            self.display_image()

    def subtract(self):

        file_path = filedialog.askopenfilename()
        if file_path:

            second_image = Image.open(file_path)
            second_image = second_image.resize(self.edited_image.size)


            pixels1 = self.edited_image.load()
            pixels2 = second_image.load()
            for i in range(self.edited_image.size[0]):
                for j in range(self.edited_image.size[1]):
                    r1, g1, b1 = pixels1[i, j]
                    r2, g2, b2 = pixels2[i, j]
                    r = max(0, r1 - r2)
                    g = max(0, g1 - g2)
                    b = max(0, b1 - b2)
                    pixels1[i, j] = (r, g, b)

            self.display_image()

    def roberts(self):

        pixels = self.edited_image.load()
        width, height = self.edited_image.size
        for i in range(width - 1):
            for j in range(height - 1):

                pixel1 = pixels[i, j]
                pixel2 = pixels[i + 1, j + 1]

                diff_r = abs(pixel1[0] - pixel2[0])
                diff_g = abs(pixel1[1] - pixel2[1])
                diff_b = abs(pixel1[2] - pixel2[2])

                pixels[i, j] = (diff_r, diff_g, diff_b)
        self.display_image()

    def save_image(self):
            self.edited_image.save("new_image.jpg")

    def cancel_changes(self):
        self.edited_image = self.original_image.copy()
        self.display_image()

root = Tk()
editor = ImageEditor(root)
root.mainloop()
