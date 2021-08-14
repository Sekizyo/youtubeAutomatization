from PIL import Image


class Formater():
    def openImage(self, path):
        try:
            image = Image.open(f'{path}')
            return image
        except:
            raise

    def cropImage(self, image):
        width, height = self.makeEvenSize(image.size)

        image.crop((0, 0, width, height))
        return image

    def makeEvenSize(self, size):
        width, height = size

        width = self.makeEven(width)
        height = self.makeEven(height)
        
        return width, height

    def makeEven(self, number):
        if self.checkIfEven(number):
            return number
        else:
            number -= 1
            return number

    def checkIfEvenTuple(self, numbers):
        if self.checkIfEven(numbers[0]) and self.checkIfEven(numbers[1]):
            return True
        else:
            return False

    def checkIfEven(self, number):
        if number%2 == 0:
            return True
        else:
            return False

    def saveImage(self, image, path):
        try:
            image.save(path)
        except:
            raise

    def run(self, path):
        image = self.openImage(path)
        if self.checkIfEvenTuple(image.size):
            croppedImage = self.cropImage(image)
            self.saveImage(croppedImage, path)