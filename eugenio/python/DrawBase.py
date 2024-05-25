import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import numpy as np
import os
from BeamBase import BeamBase

class Draw():
    def __init__(self, xDim, yDim):
        self.xDim = xDim
        self.yDim = yDim
        self.Figure = plt.figure(figsize = (xDim/yDim*8, 8))

    def DrawRectangule(self, xMin, yMin, xMax, yMax, colorLine = 'black'):
        plt.plot([xMin, xMin], [yMin, yMax], color = colorLine)
        plt.plot([xMin, xMax], [yMin, yMin], color = colorLine)
        plt.plot([xMin, xMax], [yMax, yMax], color = colorLine)
        plt.plot([xMax, xMax], [yMin, yMax], color = colorLine)

    def DrawCircle(self, center, radius, color='black'):
        circle = plt.Circle(center, radius, color=color, fill=False)
        plt.gca().add_patch(circle)

    def Plot(self):
        plt.xlim(-2, self.xDim + 2)
        plt.ylim(-2, self.yDim + 2)

    def SaveFig(self):
        # Generate a unique filename using timestamp
        unique_filename = f"file_{int(time.time())}.png"
        # Get the directory where the Python file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the "images" directory within the current directory
        images_dir = os.path.join(current_dir, "images")
        # Create the "images" directory if it doesn't exist
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        # Construct the save path within the "images" directory
        save_path = os.path.join(images_dir, unique_filename)        
    
        # Plot and save
        self.Plot()
        self.Figure.savefig(save_path)
    
        print(f"Figure saved at: {save_path}")
    
        plt.close(self.Figure)  # Close the figure explicitly
    
        return save_path  # Return the path to the saved image
            
class DrawBeam(Draw):
    def __init__(self, beamBase):
        self.Beam = beamBase
        super().__init__(beamBase.Width, beamBase.Height)

    def DrawBeam(self, drawArmor, writeDim):
        self.DrawRectangule(0, 0, self.Beam.Width, self.Beam.Height)
        if (drawArmor):
            self.DrawArmor(writeDim)

    def DrawArmor(self, writeDim):
        self.DrawRectangule(0 + self.Beam.Covering, 0 + self.Beam.Covering, self.Beam.Width - self.Beam.Covering, self.Beam.Height - self.Beam.Covering, "red")
        self.DrawRectangule(0 + self.Beam.Covering + self.Beam.DEstribo,
                            0 + self.Beam.Covering + self.Beam.DEstribo,
                            self.Beam.Width - self.Beam.Covering - self.Beam.DEstribo,
                            self.Beam.Height - self.Beam.Covering - self.Beam.DEstribo, "red")

        for i in self.Beam.GetBarArmorList():
            self.DrawCircle(i.Center, i.Radius)
        