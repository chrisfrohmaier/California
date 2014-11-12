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

####Info on matched candidate.

Is it worth having an additional column in this table that states which candidate it was matched to?
- Does each candidate have a unique ID?
	- If so, then just have an `ID of Match` column
		- If not matched, have Null or equivalent
or
- Do we want many more columns in this table with the matched candidate info?

#Match Analysis
We matched the subtraction candidates and the fakes. We found that all the candidates fell within 1" of the position the fake was inserted at (when scaled by the seeing).
![ScreenShot](https://dl.dropboxusercontent.com/u/37570643/Both_Separation_Histogram.jpg)
>Left: Distribution of the candidate/fake separation. Right: The Magnitude difference between the fake and matching candidate against the fake's magnitude. Note the offset anf the scatter.

##Problem with the Magnitude Differences
From the right panel of the above figure it is clear there is a constant offset and a large random scatter in the magnitude difference. The expected behaviour would be for a small scatter around y=0 for the brighter object with an increasing scatter as we go to fainter magnitudes.

##Further Analysis
We only looked at the data from the same night, on the same chip but across all of the V1-V10. Unfortunately the the scatter remains. It is unclear why.
![ScreenShot](https://dl.dropboxusercontent.com/u/37570643/Magdiff_Graphs/2010_05_C09.png)
###Hostless
We also looked at this trend for the hostless fakes. We suffered from poor statistics because only 10% of fakes are hostless. Again, there is scatter.
![ScreenShot](https://dl.dropboxusercontent.com/u/37570643/Magdiff_Graphs/2011_06_C02_Hostless.png)

###Possible Solution
The magnitudes for the subtraction are calculated from the zeropoint of the reference. However, I did not know these zeropoints when i was calculating the fake magnitudes. Therefore my magnitudes need to be corrected. An extra column will be added to the database with the corrected fake magnitudes. These changes won't be huge and we will still have enough object in the magnitude bins.

####Zeropoint Explanation
The `ref` has a zeropoint
The `new` has a zeropoint
These zeropoints differ by a factor (given in the subtraction table/database)
The zeropoints for the subtraction are resolved with this correction factor as follows:
![Equation](https://dl.dropboxusercontent.com/u/37570643/zp_factor.png)