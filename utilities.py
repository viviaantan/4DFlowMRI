import vtk
from vmtk import vtkvmtk, vmtkscripts
import numpy as np
from glob import glob

############ Read Dicom Folder ############
def ReadDicomFiles(FolderName):
	FileList=sorted(glob("%s/*.dcm"%FolderName))
	print (FileList[0])
	Image=vmtkscripts.vmtkImageReader()
	print (dir(Image))
	exit(1)
	Image.InputFileName(FileList[0])
	Image.ImageOutputFileName("/Users/mokhan/GoogleDrive/Owais/Research_Postdoc/perfusion_project/Simvascular/CABG1A/Images/abc.vti")
	Image.Update()

#ReadDicomFiles("/Users/mokhan/GoogleDrive/Owais/Research_Postdoc/perfusion_project/Simvascular/CABG1A/Images/CTA")

	
	

############ Input/Output ##################
def ReadVTUFile(FileName):
	reader=vtk.vtkXMLUnstructuredGridReader()
	reader.SetFileName(FileName)
	reader.Update()
	return reader.GetOutput()

def ReadVTPFile(FileName):
	reader=vtk.vtkXMLPolyDataReader()
	reader.SetFileName(FileName)
	reader.Update()
	return reader.GetOutput()

def ReadVTIFile(FileName):
	reader = vtk.vtkXMLImageDataReader() 
	reader.SetFileName(FileName) 
	reader.Update()
	return reader.GetOutput()

def WriteVTUFile(FileName,Data):
	writer=vtk.vtkXMLUnstructuredGridWriter()
	writer.SetFileName(FileName)
	writer.SetInputData(Data)
	writer.Update()
        
def WriteVTPFile(FileName,Data):
	writer=vtk.vtkXMLPolyDataWriter()
	writer.SetFileName(FileName)
	writer.SetInputData(Data)
	writer.Update()

def WriteVTIFile(FileName,Data):
	writer=vtk.vtkXMLImageDataWriter()
	writer.SetFileName(FileName)
	writer.SetInputData(Data)
	writer.Update()
	

############# Mesh Morphing Functions ###############
        #Create a line from apex and centroid of the myocardium
        
def CreateLine(Point1,Point2,Length):
	line0=np.array([Point1[0]-Point2[0],Point1[1]-Point2[1],Point1[2]-Point2[2]])
	line1=-1*line0
	line0=(line0/np.linalg.norm(line0))*(Length/2.)
	line1=(line1/np.linalg.norm(line1))*(Length/2.)
	return line0,line1

def CreatePolyLine(Coords):
	# Create a vtkPoints object and store the points in it
	points = vtk.vtkPoints()
	for i in range(len(Coords)): points.InsertNextPoint(Coords[i])

	#Create a Polyline
	polyLine = vtk.vtkPolyLine()     
	polyLine.GetPointIds().SetNumberOfIds(len(Coords))
	for i in range(len(Coords)): polyLine.GetPointIds().SetId(i, i)

	# Create a cell array to store the lines in and add the lines to it
	cells = vtk.vtkCellArray()
	cells.InsertNextCell(polyLine)

	# Create a polydata to store everything in
	polyData = vtk.vtkPolyData()
    
	# Add the points to the dataset
	polyData.SetPoints(points)

	# Add the lines to the dataset
	polyData.SetLines(cells)
	
	return polyData 

def ClosestPoint(Point, Array):
	dist_2 = np.sum((Array - Point)**2, axis=1)
	return Array[np.argmin(dist_2)],np.argmin(dist_2)

def FurthestPoint(Point, Array):
        dist_2 = np.sum((Array - Point)**2, axis=1)
        return Array[np.argmax(dist_2)],np.argmax(dist_2)

        
def ClippedSlices(Origin,Norm,Volume):
	plane=vtk.vtkPlane()
	plane.SetOrigin(Origin)
	plane.SetNormal(Norm)
	Slice=vtk.vtkCutter()
	Slice.GenerateTrianglesOff()
	Slice.SetCutFunction(plane)
	Slice.SetInputData(Volume)
	Slice.Update()
	return Slice.GetOutput()



def CutPolyData(Point1,Point2,Slice,Norm1):
	#Get the two in-plane normals
	Norm2_slice=(Point1-Point2)/np.linalg.norm(Point1-Point2)
	Norm3_slice=np.cross(Norm1,Norm2_slice)
	#Generate the two planes
	plane_N2=vtk.vtkPlane()
	plane_N2.SetOrigin(Point2)
	plane_N2.SetNormal(Norm2_slice)
	plane_N3=vtk.vtkPlane()
	plane_N3.SetOrigin(Point2)
	plane_N3.SetNormal(Norm3_slice)
	#Clip the plane to get a line across the diameter
	Line =vtk.vtkCutter()
	Line.GenerateTrianglesOff()
	Line.SetCutFunction(plane_N3)
	Line.SetInputData(Slice)
	Line.Update()
                
	#Separate the line into only one quarter (i.e. half the line)
	Line1=vtk.vtkClipPolyData()
	Line1.SetClipFunction(plane_N2)
	Line1.SetInputData(Line.GetOutput())
	Line1.Update()
	Line1_data=Line1.GetOutput()
	
	return Line1

#Get Centroid of the VTK dataset
def GetCentroid(Surface):
	Centroid=vtk.vtkCenterOfMass()
	Centroid.SetInputData(Surface)
	Centroid.SetUseScalarsAsWeights(False)
	Centroid.Update()
	return Centroid.GetCenter()


def ExtractSurface(volume):
	#Get the outer surface of the volume
	surface=vtk.vtkDataSetSurfaceFilter()
	surface.SetInputData(volume)
	surface.Update()
	return surface.GetOutput()
        
#Print the progress of the loop
def PrintProgress(self,i,N,progress_old):
	progress_=(int((float(i)/N*100+0.5)))
	if progress_%10==0 and progress_%10!=progress_old: print ("    Progress: %d%%"%progress_)
	return progress_%10

################ Direction Function ###########
#This function will extract the direction from a
#block of receptive field.
#def DirectionVector(Image,Point,BoxSize):
	



	






