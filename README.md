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

#Database 
Our fake star catalog and candidates need to be matched.
In the directory:
```
/project/projectdirs/deepsky/rates/effs/Chris_Dev/Results_V0/Fake_Star_Catalog/ 
```
There are all the catalogs for the Fake Stars which detail the variables that describe that fake object.
Each file `PTF*.w_Fake_Star_Catalog_V?.dat` is the catalog for the seperate image.

##Query
We should write a script that reads in each file and adds all the useful columns to a new database. We need to add extra columns to include the filename that matches the candidate and the version number.
###Splitting the filename.
File: `PTF201212204431_2_o_7384_10.w_Fake_Star_Catalog_V0.dat`

`ln=file.split('.')`

Now:
`ln[0]` will match with Candidate file name, `ln[1].split('_')[-1]` is the Version (we can either use `V0` or `0` for the version identifier.

###Extra Columns
`Filename` `Version` `Found (Bool)`

Should we enforce a 'found to within 1pixel' requirement for `Found` to be `True`?

or

Have a coulmn which states the distance to the nearest candidate and then we can specify later to be `<=1` when querying for efficiencies?

or both!