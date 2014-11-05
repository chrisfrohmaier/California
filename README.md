#California
All the work done in California will be added to this repository.
This should include:
- Galaxy creation script
	- Ultimate aim of this script is to calculate the flux ratios between the host and the Supernova
	
- Subtractions
	- Scripts to reorgainse the directory structure
	- Scripts to run the subtractions
	- Database stuff
	
#How to perform the subtractions
This is the directory structure of for the subtractions. (Start /project/projectdirs/deepsky/rates/effs/)

```
|-subs/
|-- 2009_01/
|--- C00
|---- V0
|---- V1
|---- ...
|---- V10
|--- ...
|--- C11
```
- Repeat this structure for 2010 and 2011
- Copy over the fakes_V? to their appropriate folder
- Copy the reference images to the appropriate from this directory"
```
/project/projectdirs/deepsky/rates/effs/refs/Rband/ptf_100019/C??
```
- Run the `mkweight` and `diffem` scripts from this directory:
```
/project/projectdirs/deepsky/rates/effs/utils/
```
- Hope that it works!
- Load the database
##Subtraction Example

![ScreenShot](https://dl.dropboxusercontent.com/u/37570643/PhD/Subtraction_Example.png)
>Left: New with fakes inserted, Middle: Ref, Right: Subtraction with fakes circled