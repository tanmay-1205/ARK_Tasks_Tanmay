#Creating a Finite State Machine

import numpy as np
import matplotlib.pyplot as plt

# Define InitializationError exception class
class InitializationError(Exception):
    pass


def rotate_image(image, angle):
    rotated_image = np.rot90(image, k=angle // 90)
    return rotated_image

class StateMachine:
    
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise  InitializationError("at least one state must be an end_state")
    
        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                print("reached ", newState)
            
                break 
            else:
                handler = self.handlers[newState.upper()]



def initialization_handler(cargo):
    print("Please enter the values of x, y, z")
    
    x = int(input("x is: "))
    y = int(input("y is: "))
    z = int(input("z is: "))

    print("Please enter rotation angles for each face")
    
    ang_1 = int(input("RG face rotation angle (0, 90, 180, 270): "))
    ang_2 = int(input("GB face rotation angle (0, 90, 180, 270): "))
    ang_3 = int(input("BR face rotation angle (0, 90, 180, 270): "))

    print("Please enter the price you want to pay:")
    price = int(input())

    # Store the user inputs and pass them to the procession handler
    inputs = {
        'x': x,
        'y': y,
        'z': z,
        'ang_1': ang_1,
        'ang_2': ang_2,
        'ang_3': ang_3,
        'price': price
    }
    newState = 'Procession'
    return (newState , inputs)


def procession_handler(inputs):
    x = inputs['x']
    y = inputs['y']
    z = inputs['z']
    ang_1 = inputs['ang_1']
    ang_2 = inputs['ang_2']
    ang_3 = inputs['ang_3']
    price = inputs['price']


    r_face = np.zeros((16,16,3), dtype = np.uint8)
    g_face = np.zeros((16,16,3), dtype = np.uint8)
    b_face = np.zeros((16,16,3), dtype = np.uint8)
    rg_face = np.zeros((16,16,3), dtype = np.uint8)
    gb_face = np.zeros((16,16,3), dtype = np.uint8)
    br_face = np.zeros((16,16,3), dtype = np.uint8)

    #Randomly assign permutations to r_face,g_face adn b_face

    r_face[:,:,0] = np.random.permutation(np.arange(256)).reshape((16, 16))
    g_face[:,:,1] = np.random.permutation(np.arange(256)).reshape((16, 16))
    b_face[:,:,2] = np.random.permutation(np.arange(256)).reshape((16, 16))
        
    #Now to pixelate rg_face , gb_face and br_face 

    #FOR RG_FACE
    for p in range(16):
        for q in range(16):
            intensity_r = r_face[x, p, 0]
            intensity_g = g_face[y, q, 1]
            rg_face[p, q] = [intensity_r, intensity_g, 0]

    #FOR GB_FACE
    for q in range(16):
        for r in range(16):
            intensity_g = g_face[y, q, 1]
            intensity_b = b_face[z, r, 2]
            gb_face[q, r] = [0, intensity_g, intensity_b]

    for r in range(16):
        for p in range(16):
            intensity_b = b_face[z, r, 2]
            intensity_r = r_face[x, p, 0]
            br_face[r, p] = [intensity_r, 0, intensity_b]

    #Now we need to rotate all three faces 

    rg_face = rotate_image(rg_face, ang_1)
    gb_face = rotate_image(gb_face , ang_2)
    br_face = rotate_image(br_face , ang_3)

    newState = 'Display'
    inputs_ = {
        'rg_face': rg_face,
        'gb_face': gb_face,
        'br_face': br_face,
        'price': price
    }

    return ( newState , inputs_)

def display_handler( inputs_ ):

    rg_face = inputs_['rg_face']
    gb_face = inputs_['gb_face']
    br_face = inputs_['br_face']
    price = inputs_['price']
    
    if(price >=60):
        fig, axs = plt.subplots(1, 3)
        axs[0].imshow(rg_face)
        axs[0].axis('off')
        axs[1].imshow(gb_face)
        axs[1].axis('off')
        axs[2].imshow(br_face)
        axs[2].axis('off')
        plt.show()

        print()
        print(f"The remaining money left: {price-60}")

    elif((price >= 20) and ( price < 40)) :

        print("Only one face can be printed")
        print()
        face = input("Which face should be shown?(rg_face/gb_face/br_face)")
        if( face == 'rg_face'):
            plt.imshow(rg_face)
            plt.title("RG face")
           
        elif( face == 'gb_face'):
            plt.imshow(gb_face)
            plt.title("GB face")
            
        elif( face == 'br_face'):
            plt.imshow(br_face)
            plt.title("BR face")
        plt.axis('off')
        plt.show()
        print()
        print(f"The remaining money left: {price -20} ")

    elif((price >=40) and (price<60)):

        print("Two faces can be printed")
        print()
        face_1 = input("1st face to be shown?(rg_face/gb_face/br_face)")

        if( face_1 == 'rg_face'):
            plt.imshow(rg_face)
            plt.title("RG face")
    
        elif( face_1 == 'gb_face'):
            plt.imshow(gb_face)
            plt.title("GB face")
            
        elif( face_1 == 'br_face'):
            plt.imshow(br_face)
            plt.title("BR face")
        
        plt.axis('off')
        plt.show()

        face_2 = input("2nd face to be shown?(rg_face/gb_face/br_face)")

        if( face_2 == 'rg_face'):
            plt.imshow(rg_face)
            plt.title("RG face")
            
        elif( face_2 == 'gb_face'):
            plt.imshow(gb_face)
            plt.title("GB face")
           
        elif( face_2 == 'br_face'):
            plt.imshow(br_face)
            plt.title("BR face")
        plt.axis('off')
        plt.show()

        print()
        print(f"The remaining money left: {price -40} ")

    elif( price < 20):
        print("No images can be displayed.")
        print(f"The remaining money left: {price}")

    return ('endDisplay',inputs_)

def end_display_handler(inputs_):
    print("Hallo")
    return ("neg_state", "")
        
def main():
    fsm = StateMachine()
    fsm.add_state("Initialization", initialization_handler)
    fsm.add_state("Procession", procession_handler)
    fsm.add_state("Display",display_handler)
    fsm.add_state("endDisplay",end_display_handler,1)
    fsm.set_start("Initialization")
    fsm.run("Initial cargo")

if __name__ == "__main__":
    main()