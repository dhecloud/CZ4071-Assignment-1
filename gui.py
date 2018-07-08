import os
import tkinter as tk
import json
from PIL import ImageTk, Image


def read_properties():
    with open('analysis/BA.txt','r') as f:
        BAp = str(f.readlines())
    f.close()
    BAp = (BAp.replace('[','').replace(']','').replace("'",'')).split(',')
    with open('analysis/RN.txt','r') as f:
        RNp = str(f.readlines())
    f.close()
    RNp = (RNp.replace('[','').replace(']','').replace("'",'')).split(',')
    with open('analysis/SF.txt','r') as f:
        SFp = str(f.readlines())
    f.close()
    SFp = (SFp.replace('[','').replace(']','').replace("'",'')).split(',')
    with open('analysis/MODEL.txt','r') as f:
        MODELp = str(f.readlines())
    f.close()
    MODELp = (MODELp.replace('[','').replace(']','').replace("'",'')).split(',')
    return [MODELp, RNp, BAp, SFp]
    
    
class MainApp:
    def __init__(self, master, p):
        self.master = master
        self.model, self.RN, self.BA, self.SF = p
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'View TPC-H Properties', width = 50, command = self.new_window_model)
        self.button1.pack()
        self.button2 = tk.Button(self.frame, text = 'View Random Network (RN) properties', width = 50, command = self.new_window_RN)
        self.button2.pack()
        self.compareButton1 = tk.Button(self.frame, text = "Compare RN properties with TPC-H's", width = 50, command = self.compare_RN_with_model)
        self.compareButton1.pack()      
        self.button3 = tk.Button(self.frame, text = 'View Scale Free (SF) properties', width = 50, command = self.new_window_SF)
        self.button3.pack()
        self.compareButton2 = tk.Button(self.frame, text = "Compare SF properties with TPC-H's", width = 50, command = self.compare_SF_with_model)
        self.compareButton2.pack()      
        self.button4 = tk.Button(self.frame, text = 'View Barabasi-Albert (BA) properties', width = 50, command = self.new_window_BA)
        self.button4.pack()
        self.compareButton3 = tk.Button(self.frame, text = "Compare BA properties with TPC-H's", width = 50, command = self.compare_BA_with_model)
        self.compareButton3.pack()     
        self.visualizeButton = tk.Button(self.frame, text = "Visualize the TPC-H network's largest hub", width = 50, command = self.visualize_model)
        self.visualizeButton.pack()      
        self.frame.pack()

    def new_window_model(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = ModelProperties(self.newWindow, self.model)
    
    def new_window_RN(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = RNProperties(self.newWindow, self.RN)
        
    def new_window_SF(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = SFProperties(self.newWindow, self.SF)
        
    def new_window_BA(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = BAProperties(self.newWindow, self.BA)
        
    def compare_BA_with_model(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = CompareBA(self.newWindow, self.model, self.BA)

    def compare_SF_with_model(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = CompareSF(self.newWindow, self.model, self.SF)
    
    def compare_RN_with_model(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = CompareRN(self.newWindow, self.model, self.RN)
        
    def visualize_model(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = VisualizeModel(self.newWindow)


class VisualizeModel:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.path = "graph/subgraph.png"
        self.img = ImageTk.PhotoImage(Image.open(self.path))
        self.panel = tk.Label(self.frame, image = self.img)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
        
    def close_windows(self):
        self.master.destroy()
        
        
class ModelProperties:
    def __init__(self, master, p):
        self.master = master
        self.kin = [0,0,0,0]
        self.degdist = [0,0,0,0]
        self.dmax, self.kin[0], self.kin[1], self.kin[2], self.kin[3], self.degdist[0],self.degdist[1],self.degdist[2],self.degdist[3], self.numnodes, self.acc, self.apl = p
        self.frame = tk.Frame(self.master)
        self.degdis_Text = tk.Text(self.frame, height=4,width=100)
        self.degdis_Text.insert(tk.INSERT,'TPC-H degree distribution for k = ' + str(self.kin[0]) + ' is approximately' + str(self.degdist[0]) +  '\n')
        self.degdis_Text.insert(tk.INSERT,'TPC-H degree distribution for k = ' + str(self.kin[1]) + ' is approximately' + str(self.degdist[1]) +  ' \n')
        self.degdis_Text.insert(tk.INSERT,'TPC-H degree distribution for k = ' + str(self.kin[2]) + ' is approximately' + str(self.degdist[2]) +  '\n')
        self.degdis_Text.insert(tk.INSERT,'TPC-H degree distribution for k = ' + str(self.kin[3]) + ' is approximately'+ str(self.degdist[3]))
        self.degdis_Text.pack()
        self.apl_Text = tk.Text(self.frame, height=2,width=100)
        self.apl_Text.insert(tk.INSERT,'TPC-H average path length for N = ' +  str(self.numnodes) + 'is expected to be '+ str(self.apl))
        self.apl_Text.pack()
        self.acc_Text = tk.Text(self.frame, height=2,width=100)
        self.acc_Text.insert(tk.INSERT,'TPC-H average clustering coefficient for N = ' +  str(self.numnodes)  + ' is expected to be ' + str(self.acc))
        self.acc_Text.pack()  
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
        
    def close_windows(self):
        self.master.destroy()
        
        
class BAProperties:
    def __init__(self, master, p):
        self.master = master
        self.degdist = [0,0,0,0]
        self.numnodes, self.degdist[0],self.degdist[1],self.degdist[2],self.degdist[3], self.apl, self.acc, self.dia = p
        self.frame = tk.Frame(self.master)
        self.degdis_Text = tk.Text(self.frame, height=4,width=100)
        self.degdis_Text.insert(tk.INSERT,'BA degree distribution for k = 1 is expected to be' + str(self.degdist[0]) +  '\n')
        self.degdis_Text.insert(tk.INSERT,'BA degree distribution for k = 2 is expected to be' + str(self.degdist[1]) +  ' \n')
        self.degdis_Text.insert(tk.INSERT,'BA degree distribution for k = 3 is expected to be' + str(self.degdist[2]) +  '\n')
        self.degdis_Text.insert(tk.INSERT,'BA degree distribution for k = 4 is expected to be'+ str(self.degdist[3]))
        self.degdis_Text.pack()
        self.apl_Text = tk.Text(self.frame, height=2,width=100)
        self.apl_Text.insert(tk.INSERT,'BA average path length for N = ' +  str(self.numnodes) + 'is expected to be '+ str(self.apl))
        self.apl_Text.pack()
        self.dia_Text = tk.Text(self.frame, height=2,width=100)
        self.dia_Text.insert(tk.INSERT,'BA diameter for N = ' +  str(self.numnodes)  + 'is expected to be '+ str(self.dia))
        self.dia_Text.pack()
        self.acc_Text = tk.Text(self.frame, height=2,width=100)
        self.acc_Text.insert(tk.INSERT,'BA average clustering coefficient for N = ' +  str(self.numnodes)  + ' is expected to be ' + str(self.acc))
        self.acc_Text.pack()  
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
        
    def close_windows(self):
        self.master.destroy()

class RNProperties:
    def __init__(self, master, p):
        self.master = master
        self.degdist = [0,0,0,0]
        self.numnodes, self.degdist[0],self.degdist[1],self.degdist[2],self.degdist[3], self.apl, self.acc= p
        self.frame = tk.Frame(self.master)
        self.degdis_Text = tk.Text(self.frame, height=4,width=100)
        self.degdis_Text.insert(tk.INSERT,'RN degree distribution for k = 1 is expected to be' + str(self.degdist[0]) +  '\n')
        self.degdis_Text.insert(tk.INSERT,'RN degree distribution for k = 2 is expected to be' + str(self.degdist[1]) +  ' \n')
        self.degdis_Text.insert(tk.INSERT,'RN degree distribution for k = 3 is expected to be' + str(self.degdist[2]) +  '\n')
        self.degdis_Text.insert(tk.INSERT,'RN degree distribution for k = 4 is expected to be'+ str(self.degdist[3]))
        self.degdis_Text.pack()
        self.apl_Text = tk.Text(self.frame, height=2,width=100)
        self.apl_Text.insert(tk.INSERT,'RN average path length for N = ' +  str(self.numnodes) + 'is expected to be '+ str(self.apl))
        self.apl_Text.pack()
        self.acc_Text = tk.Text(self.frame, height=2,width=100)
        self.acc_Text.insert(tk.INSERT,'RN average clustering coefficient for N = ' +  str(self.numnodes)  + ' is expected to be ' + str(self.acc))
        self.acc_Text.pack()  
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
        
    def close_windows(self):
        self.master.destroy()

class SFProperties:
    def __init__(self, master, p):
        self.master = master
        self.degdist = [0,0,0,0]
        self.numnodes, self.degdist[0],self.degdist[1],self.degdist[2],self.degdist[3], self.apl, self.hub = p
        self.frame = tk.Frame(self.master)
        self.degdis_Text = tk.Text(self.frame, height=4,width=100)
        self.degdis_Text.insert(tk.INSERT,'SF degree distribution for k = 1 is expected to be' + str(self.degdist[0]) +  '\n')
        self.degdis_Text.insert(tk.INSERT,'SF degree distribution for k = 2 is expected to be' + str(self.degdist[1]) +  ' \n')
        self.degdis_Text.insert(tk.INSERT,'SF degree distribution for k = 3 is expected to be' + str(self.degdist[2]) +  '\n')
        self.degdis_Text.insert(tk.INSERT,'SF degree distribution for k = 4 is expected to be'+ str(self.degdist[3]))
        self.degdis_Text.pack()
        self.apl_Text = tk.Text(self.frame, height=2,width=100)
        self.apl_Text.insert(tk.INSERT,'SF average path length for N = ' +  str(self.numnodes) + ' is expected to be '+ str(self.apl))
        self.apl_Text.pack()
        self.hub_Text = tk.Text(self.frame, height=2,width=100)
        self.hub_Text.insert(tk.INSERT,'SF size of largest hub for N = ' +  str(self.numnodes)  + ' is expected to be ' + str(self.hub))
        self.hub_Text.pack()  
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
        
    def close_windows(self):
        self.master.destroy()

class CompareBA:
    def __init__(self, master, model, BA):
        #self.numnodes, self.degdist[0],self.degdist[1],self.degdist[2],self.degdist[3], self.apl, self.acc, self.dia 
        self.kinmodel = [0,0,0,0]
        self.degdistmodel = [0,0,0,0]
        self.dmax, self.kinmodel[0], self.kinmodel[1], self.kinmodel[2], self.kinmodel[3], self.degdistmodel[0],self.degdistmodel[1],self.degdistmodel[2],self.degdistmodel[3], self.numnodesmodel, self.accmodel, self.aplmodel = model
        self.degdistBA = [0,0,0,0]
        self.numnodesBA, self.degdistBA[0],self.degdistBA[1],self.degdistBA[2],self.degdistBA[3], self.aplBA, self.accBA, self.diaBA = BA
        self.master = master
        self.frame = tk.Frame(self.master)
        self.hub_Text = tk.Text(self.frame, height=4,width=30)
        self.hub_Text.insert(tk.INSERT,'numnodes = Number of Nodes\n')
        self.hub_Text.grid() 
        self.hub_Text.insert(tk.INSERT,'apl = Average Path Length\n')
        self.hub_Text.grid() 
        self.hub_Text.insert(tk.INSERT,'acc = Average Clustering Coeff\n')
        self.hub_Text.grid() 
        
        #headers 
        self.l = tk.Label(self.frame,text="     ",width = 35)
        self.l.grid(row=1,column=2)
        self.l1 = tk.Label(self.frame,text=" TPC-H ", relief=tk.SOLID,width = 35)
        self.l1.grid(row=1,column=3)
        self.l2 = tk.Label(self.frame,text="  BA  ", relief=tk.SOLID,width = 35)
        self.l2.grid(row=1,column=5)
        #properties
        self.nodes = tk.Label(self.frame,text=" numnodes ", relief=tk.SOLID,width = 35)
        self.nodes.grid(row=2,column=2)
        self.apl = tk.Label(self.frame,text="       apl       ", relief=tk.SOLID,width = 35)
        self.apl.grid(row=3,column=2)
        self.acc = tk.Label(self.frame,text="      acc       ", relief=tk.SOLID,width = 35)
        self.acc.grid(row=4,column=2)
        
        #model values
        self.nodesmodel = tk.Label(self.frame,text=self.numnodesmodel, relief=tk.RIDGE, width = 35)
        self.nodesmodel.grid(row=2,column=3)
        self.apl = tk.Label(self.frame,text=self.aplmodel, relief=tk.RIDGE,width = 35)
        self.apl.grid(row=3,column=3)
        self.acc = tk.Label(self.frame,text=self.accmodel, relief=tk.RIDGE,width = 35)
        self.acc.grid(row=4,column=3)
        
        #theoretical values
        self.nodesBA = tk.Label(self.frame,text=self.numnodesBA, relief=tk.RIDGE, width = 35)
        self.nodesBA.grid(row=2,column=5)
        self.apl = tk.Label(self.frame,text=self.aplBA, relief=tk.RIDGE,width = 35)
        self.apl.grid(row=3,column=5)
        self.acc = tk.Label(self.frame,text=self.accBA, relief=tk.RIDGE,width = 35)
        self.acc.grid(row=4,column=5)
        
        
        self.path = "graph/degree_his_model.png"
        self.img1 = ImageTk.PhotoImage(Image.open(self.path).resize((310,350)))
        self.panel1 = tk.Label(self.frame, image = self.img1)
        self.panel1.grid(row=6,column=3)
        
        self.path = "graph/degree_his_BA.png"
        self.img2 = ImageTk.PhotoImage(Image.open(self.path).resize((310,350)))
        self.panel2 = tk.Label(self.frame, image = self.img2)
        self.panel2.grid(row=6,column=5)

        self.frame.grid()

    def close_windows(self):
        self.master.destroy()

class CompareRN:
    def __init__(self, master, model, RN):
        #self.numnodes, self.degdist[0],self.degdist[1],self.degdist[2],self.degdist[3], self.apl, self.hub = p
        self.degdistmodel = [0,0,0,0]
        self.kinmodel = [0,0,0,0]
        self.dmax, self.kinmodel[0], self.kinmodel[1], self.kinmodel[2], self.kinmodel[3], self.degdistmodel[0],self.degdistmodel[1],self.degdistmodel[2],self.degdistmodel[3], self.numnodesmodel, self.accmodel, self.aplmodel = model
        self.degdistRN = [0,0,0,0]
        self.numnodesRN, self.degdistRN[0],self.degdistRN[1],self.degdistRN[2],self.degdistRN[3], self.aplRN, self.accRN = RN
        self.master = master
        self.frame = tk.Frame(self.master)
        self.hub_Text = tk.Text(self.frame, height=4,width=30)
        self.hub_Text.insert(tk.INSERT,'numnodes = Number of Nodes\n')
        self.hub_Text.grid() 
        self.hub_Text.insert(tk.INSERT,'apl = Average Path Length\n')
        self.hub_Text.grid() 
        self.hub_Text.insert(tk.INSERT,'acc= Average Clustering Coeff\n')
        self.hub_Text.grid() 
        
        #headers 
        self.l = tk.Label(self.frame,text="     ",width = 35)
        self.l.grid(row=1,column=2)
        self.l1 = tk.Label(self.frame,text=" TPC-H ", relief=tk.SOLID,width = 35)
        self.l1.grid(row=1,column=3)
        self.l2 = tk.Label(self.frame,text="  RN  ", relief=tk.SOLID,width = 35)
        self.l2.grid(row=1,column=5)
        
        #properties
        self.nodes = tk.Label(self.frame,text=" numnodes ", relief=tk.SOLID,width = 35)
        self.nodes.grid(row=2,column=2)
        self.apl = tk.Label(self.frame,text="       apl       ", relief=tk.SOLID,width = 35)
        self.apl.grid(row=3,column=2)
        self.acc = tk.Label(self.frame,text="      acc      ", relief=tk.SOLID,width = 35)
        self.acc.grid(row=4,column=2)
        
        #model values
        self.nodesmodel = tk.Label(self.frame,text=self.numnodesmodel, relief=tk.RIDGE, width = 35)
        self.nodesmodel.grid(row=2,column=3)
        self.apl = tk.Label(self.frame,text=self.aplmodel, relief=tk.RIDGE,width = 35)
        self.apl.grid(row=3,column=3)
        self.acc = tk.Label(self.frame,text=self.accmodel, relief=tk.RIDGE,width = 35)
        self.acc.grid(row=4,column=3)
        
        #theoretical values
        self.nodesBA = tk.Label(self.frame,text=self.numnodesRN, relief=tk.RIDGE, width = 35)
        self.nodesBA.grid(row=2,column=5)
        self.apl = tk.Label(self.frame,text=self.aplRN, relief=tk.RIDGE,width = 35)
        self.apl.grid(row=3,column=5)
        self.acc = tk.Label(self.frame,text=self.accRN, relief=tk.RIDGE,width = 35)
        self.acc.grid(row=4,column=5)
        
        self.path = "graph/degree_his_model.png"
        self.img1 = ImageTk.PhotoImage(Image.open(self.path).resize((310,350)))
        self.panel1 = tk.Label(self.frame, image = self.img1)
        self.panel1.grid(row=6,column=3)
        
        self.path = "graph/degree_his_RN.png"
        self.img2 = ImageTk.PhotoImage(Image.open(self.path).resize((310,350)))
        self.panel2 = tk.Label(self.frame, image = self.img2)
        self.panel2.grid(row=6,column=5)
        
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 35, command = self.close_windows)
        self.quitButton.grid(row= 100, column = 6)
        
        self.frame.grid()

    def close_windows(self):
        self.master.destroy()
                
class CompareSF:
    def __init__(self, master, model, SF):
        #self.numnodes, self.degdist[0],self.degdist[1],self.degdist[2],self.degdist[3], self.apl, self.hub = p
        self.degdistmodel = [0,0,0,0]
        self.kinmodel = [0,0,0,0]
        self.dmax, self.kinmodel[0], self.kinmodel[1], self.kinmodel[2], self.kinmodel[3], self.degdistmodel[0],self.degdistmodel[1],self.degdistmodel[2],self.degdistmodel[3], self.numnodesmodel, self.accmodel, self.aplmodel = model
        self.degdistSF = [0,0,0,0]
        self.numnodesSF, self.degdistSF[0],self.degdistSF[1],self.degdistSF[2],self.degdistSF[3], self.aplSF, self.hubSF = SF
        self.master = master
        self.frame = tk.Frame(self.master)
        self.hub_Text = tk.Text(self.frame, height=4,width=30)
        self.hub_Text.insert(tk.INSERT,'numnodes = Number of Nodes\n')
        self.hub_Text.grid() 
        self.hub_Text.insert(tk.INSERT,'apl = Average Path Length\n')
        self.hub_Text.grid() 
        self.hub_Text.insert(tk.INSERT,'Ldeg= Largest degree\n')
        self.hub_Text.grid() 
        
        #headers 
        self.l = tk.Label(self.frame,text="     ",width = 35)
        self.l.grid(row=1,column=2)
        self.l1 = tk.Label(self.frame,text=" Model ", relief=tk.SOLID,width = 35)
        self.l1.grid(row=1,column=3)
        self.l2 = tk.Label(self.frame,text="  SF  ", relief=tk.SOLID,width = 35)
        self.l2.grid(row=1,column=5)
        
        #properties
        self.nodes = tk.Label(self.frame,text=" numnodes ", relief=tk.SOLID,width = 35)
        self.nodes.grid(row=2,column=2)
        self.apl = tk.Label(self.frame,text="       apl       ", relief=tk.SOLID,width = 35)
        self.apl.grid(row=3,column=2)
        self.acc = tk.Label(self.frame,text="      Ldeg       ", relief=tk.SOLID,width = 35)
        self.acc.grid(row=4,column=2)
        
        #model values
        self.nodesmodel = tk.Label(self.frame,text=self.numnodesmodel, relief=tk.RIDGE, width = 35)
        self.nodesmodel.grid(row=2,column=3)
        self.apl = tk.Label(self.frame,text=self.aplmodel, relief=tk.RIDGE,width = 35)
        self.apl.grid(row=3,column=3)
        self.acc = tk.Label(self.frame,text=self.dmax, relief=tk.RIDGE,width = 35)
        self.acc.grid(row=4,column=3)
        
        #theoretical values
        self.nodesBA = tk.Label(self.frame,text=self.numnodesSF, relief=tk.RIDGE, width = 35)
        self.nodesBA.grid(row=2,column=5)
        self.apl = tk.Label(self.frame,text=self.aplSF, relief=tk.RIDGE,width = 35)
        self.apl.grid(row=3,column=5)
        self.acc = tk.Label(self.frame,text=self.hubSF, relief=tk.RIDGE,width = 35)
        self.acc.grid(row=4,column=5)
        
        
        self.path = "graph/degree_his_model.png"
        self.img1 = ImageTk.PhotoImage(Image.open(self.path).resize((310,350)))
        self.panel1 = tk.Label(self.frame, image = self.img1)
        self.panel1.grid(row=6,column=3)
        
        self.path = "graph/degree_his_SF.png"
        self.img2 = ImageTk.PhotoImage(Image.open(self.path).resize((310,350)))
        self.panel2 = tk.Label(self.frame, image = self.img2)
        self.panel2.grid(row=6,column=5)
        
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 35, command = self.close_windows)
        self.quitButton.grid(row= 100, column = 6)
        
        self.frame.grid()

    def close_windows(self):
        self.master.destroy()
        
def main(): 
    root = tk.Tk()
    p = read_properties()
    app = MainApp(root, p)
    app.master.title("CZ4071 TPC-H GUI")
    root.configure(background='blue')
    root.mainloop()

if __name__ == '__main__':
    print("Loading... Hang on for a minute or so..")
    os.system("python properties.py")
    print("Loading done!")
    main()