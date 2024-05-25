import matplotlib.pyplot as plt
import numpy as np

class SteelBarLine():

    def __init__(self, x, y, radius):
        self.Center = (x, y)
        self.Radius = radius
        self.Area = 0

class BeamBase():

    AgressiveCovering = [2, 3, 3, 3.5] #cm
    
    def __init__(self, width, height, agressClass, quantBar, dBar, dAgreg, dEstribo, av):
        self.Width = width  #cm
        self.Height = height #cm
        
        self.AgressClass = agressClass #adm
        self.Covering = self.CalcCovering() #cm
        
        self.QuantBar = quantBar # adm
        self.DBar = dBar #cm
        self.DAgreg = dAgreg #cm
        self.DEstribo = dEstribo #cm
        self.Av = av #cm

        self.BarConfiguration = self.CalcBarConfiguration(0, 0, 0)


    def CalcCovering(self):
        if (self.AgressClass > 3):
            return self.AgressiveCovering[3]
        return self.AgressiveCovering[self.AgressClass]
    
    def CalcMinDistBar(self):
        return max([2, self.DBar, 1.2 * self.DAgreg])

    def CalcDistBar(self, QuantBar):
        return (self.Width - (2*self.Covering + 2*self.DEstribo + QuantBar*self.DBar))/(QuantBar - 1)

    def CalcMaxBarPerLine(self, QuantInit = 2):
        QuantMax = QuantInit
        minDist = self.CalcMinDistBar()
        dist = self.CalcDistBar(QuantMax)
        
        while (dist >= minDist):
            QuantMax += 1
            dist = self.CalcDistBar(QuantMax)
            
        return (QuantMax - 1)

    def GetBarArmorList(self):
        barList = []
        for i in self.BarConfiguration:
            for j in i:
                barList.append(j)
                
        return barList

    def CalcBarConfiguration(self, idealNumber = 0, xInit = 0, yInit = 0):      
        maxNumber = self.CalcMaxBarPerLine()
        numberPerLine = idealNumber if idealNumber <= maxNumber and idealNumber != 0 else maxNumber
        numberPerLine = numberPerLine if numberPerLine <= self.QuantBar else self.QuantBar
        barList = []
        yInitial = self.Covering + self.DEstribo + self.DBar/2 if yInit == 0 else yInit
        xInitial = self.Covering + self.DEstribo + self.DBar/2 if xInit == 0 else xInit

        print((self.QuantBar//numberPerLine) + 1)
        
        for i in range(0, (self.QuantBar//numberPerLine) + 1):
            if i == 0:
                barList.append([j for j in self.DistrLineBar(numberPerLine, xInitial, yInitial, 'uniforme')])
                
            elif ( self.QuantBar%numberPerLine <= 0 and i == (self.QuantBar//numberPerLine) + 1):
                pass
            
            elif (i == (self.QuantBar//numberPerLine)):
                barList.append([j for j in self.DistrLineBar(self.QuantBar%numberPerLine, xInitial, yInitial, 'uniforme')])
                
            else:
                barList.append([j for j in self.DistrLineBar(numberPerLine, xInitial, yInitial, 'uniforme')])

            yInitial += self.Av + self.DBar
        return barList

    def CalcBarArea(self):
        xl, xr, yb, yu = 0, 0, 0, 0
        nLineBars = len(self.BarConfiguration)
        for barLineNumber in range(nLineBars):
            nColumnsBar = len(self.BarConfiguration[barLineNumber])
            for barColumnNumber in range(nColumnsBar):
        
                bar = self.BarConfiguration[barLineNumber][barColumnNumber]
                ######### YBotton
                if (barLineNumber == 0):
                    yb = self.Covering + self.DEstribo + self.DBar/2 if self.Covering + self.DEstribo + self.DBar/2 < 7.5 * self.DBar else 7.5 * self.DBar
                else:
                    yb = self.Av/2 + self.DBar/2
                ######### YTop - falta um caso
                if ((barLineNumber == nLineBars - 1)):
                    yu = self.DBar * 7.5
                else:
                    yu = self.Av/2 + self.DBar/2 if self.Av/2 + self.DBar/2 < 7.5 * self.DBar else 7.5 * self.DBar
                    
                ######### XLeft
                if (len(self.BarConfiguration[barLineNumber]) == 1):
                    xl = self.Width/2 if self.Width/2 < 7.5 * self.DBar else 7.5 * self.DBar
                elif (barColumnNumber == 0):
                    xl = self.Covering + self.DEstribo + self.DBar/2 if self.Covering + self.DEstribo + self.DBar/2 < 7.5 * self.DBar else 7.5 * self.DBar
                else:
                    xl = abs(self.BarConfiguration[barLineNumber][barColumnNumber].Center[0] - self.BarConfiguration[barLineNumber][barColumnNumber - 1].Center[0])/2

                ######## XRight
                if (len(self.BarConfiguration[barLineNumber]) == 1):
                    xr = self.Width/2 if self.Width/2 < 7.5 * self.DBar else 7.5 * self.DBar
                elif (barColumnNumber == nColumnsBar - 1):
                    xr = self.Covering + self.DEstribo + self.DBar/2 if self.Covering + self.DEstribo + self.DBar/2 < 7.5 * self.DBar else 7.5 * self.DBar
                else:
                    xr = abs(self.BarConfiguration[barLineNumber][barColumnNumber + 1].Center[0] - self.BarConfiguration[barLineNumber][barColumnNumber].Center[0])/2

                self.BarConfiguration[barLineNumber][barColumnNumber].Area = (xr + xl) * (yb + yu) #cm2
        
    def DistrLineBar(self, quantBar, xPos, yPos, distType = 'uniforme'):
        # uniforme - barras distribuídas a mesma distância
        # bordas - concentra as barras na borda
        steelBars = []
        xInit = xPos
        if (quantBar <=0):
            return steelBars

        elif (quantBar == 1):
            steelBars.append(SteelBarLine(self.Width/2, yPos, self.DBar/2))
        
        elif (distType == 'uniforme' or (not (quantBar % 2 == 0))):
            dist = self.CalcDistBar(quantBar)
            for i in range(quantBar):
                steelBars.append(SteelBarLine(xInit, yPos, self.DBar/2))
                xInit += dist + self.DBar

        else:
            dist = self.CalcMinDistBar()
            for i in range(0, quantBar//2):
                steelBars.append(SteelBarLine(xInit, yPos, self.DBar/2))
                xInit += dist + self.DBar
            xInit = self.Width - xPos
            for i in range(0, quantBar//2):
                steelBars.append(SteelBarLine(xInit, yPos, self.DBar/2))
                xInit -= (dist + self.DBar)

        return steelBars
#self, width, height, agressClass, quantBar, dBar, dAgreg, dEstribo, av):