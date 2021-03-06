# gmm
A modified version of GMM calculator first created by Y-L. Xu, https://scattport.org/files/xu/codes.htm
1. The nominal GMT (Generalised MIE Theory) package comprise of the following files 

gmm01f.f  gmm01f.in  gmm01f.par  Makefile  multiply.f90  
mycal.in  mycal.sh  visuallize_sigma.py clean.sh  experimental.dat  gen_sigma.py  

2. Mandatory requirement: gfortran. 

3. To compile the gmt code, first issue the command in the directory containing the gmt package,

	make clean
	make	 

This will generate a fresh executable 
	
	gmm01f 

gmm01f is the Generalised MIE theory program executable.

4. experimental.dat, which values are obtained independently from experiment, must have already been in existence. Wihtout this file, the package can not be run.

5. An sample experimental.dat contains the following information:

line 1: Scattering angle = 0
line 2: headings: Wavelength	Ref Index (real)	Ref Index (imaginary)	Cext	Csca	Cabs
line 3: data of   Wavelength	Ref Index (real)	Ref Index (imaginary)	Cext	Csca	Cabs

6. A file named 
	
	mycal.in

is a file containing the coordinates of N particles.

7. With presence of the files experiment.dat and mycal.in the current directory, execute 
	
	./mycal.sh

8. This will produce three output files, namely, gmt.dat, results.tmp and sigma.csv. 

9. The data in gmt.dat has the format

	line 1: scattering angle from experimental.dat: 0
	line 2:	wavelength          Cext
	line 3:	400.2083  0.10285E+00 
	line 4:	411.3093  0.10040E+00 
	...

where Cext are the values predicted by MIE theory (gmm01f) for the corresponding wavelength. The values of Cext in gmt.dat are generated based on the configuration of the particles in mycal.in. These data are generated theoretically based on the Generalised MIE theory. 

10. In mycal.sh the information of the wavelength, real and imaginary part of the reflective index contained in  experiment.dat is abstracted to prepare an intermediate file bk7s2.k, one for each wavelength. 

11. A sample of the bk7s2.k file is as follows:

##############################################################################

1000
4
37.883 55.284 	36.538 0.5 0.227 6.472
53.707 -36.886 	49.748 0.5 0.227 6.472
-48.179 18.283 -18.124 0.5 0.227 6.472
-50.410 43.813 -57.346 0.5 0.227 6.472


##############################################################################

12. The first row in bk7s2.k refers to the "wavelength". 

13. The integer in second row in bk7s2.k refers to an integer N, number of particles. This integer N is a variable that can range from 1 to 79 (the upper limit is dependent on the computer's memory).  

14. In row three or above, the lines in bk7s2.k are interpreted as followed: 

x-coordinate	   y-coordinate	       z-coordinate       radius       Re(refractive index)    Im(refractive index)

15. radius refers to the size of the particle. It is an positive variable ranging from e.g. 0.5 to say 10.0, but the actual range is not constrained as long as it is a non-zero positive value. 

16. The executable gmm01f is then executed for each wavelength-specific bk7s2.k one by one. If there are NW number of wavelength in experiment.dat, gmm01f < bk7s2.k will be performed NW times when mycal.sh is executed.

17. The process to execute gmm01f for all wavelength may take up to a few minutes if the number of NP is large. 

18. If the configuration in mycal.in contains overlapping particles, gmm01f will result in non-convergence and produce no output for the absorption coefficient for that particular wavelenth, along with a lengthy warning notification explaning that overlapping has occured. 

19. mycal.sh is designed to handle such overlapping situation. If non-convergence occur, an execption handler in mycal.sh will artificially write a value of 99999 for the value of Cext at that wavelength into gmt.dat. 

20. The wavelength vs Cext curve in experimental.dat is to be compared against that predicted by MIE theory (contained in gmt.dat). The discrepency between them is quantified in terms of sigma, the standard deviation defined based on the set of point-by-point values in these curves. Note that to calculate a meaningful standard deviation between the two curves, both have to be normalised, i.e., the value of each Cext has to be scalled by a common normalisation factor such that the area under the scaled curve is equal to 1. 

21. In mycal.sh, the normalisation procedure is implemented, in the presence of gmt.dat and experimet.dat, via

	python gen_sigma.py
	
22. The execution of gen_sigma.py produces results.tmp and sigma.csv. sigma.csv contains the normalised Cext vs wavelength data from gmt.dat and exeperimental.dat, while results.tmp contain the value of the standard deviation between the normalised GMT curve and the normlised experimental curves. 

23. The curves in sigma.csv can be visualised via 

	python visuallize_sigma.py

A sigma.png file will be produced upon manual execution of the visuallize_sigma.py code

24. If gen_sigma.py is executed and reading in a gmt.dat file that contains at least one non-convergence value of Cext (which is assigned 99999), the gmt curve will not be normalized, while the experimental Cext vs wavelength curve will still be normalised. 

25. The exceptional handling of non-convergence (overlapping scenario) will result in a large value of sigma or order >> ~10^0. If no such non-convergence occur, both curves will be normalised and a sigma value of the order ~10^0 or less will be returned. 

26. In the unlikely case where the configuration in mycal.in results in a gmt curve match exactly with that of the experiment.dat, sigma = 0. In this scenario, the configuration contained in mycal.in is said to produce an experimental FTIR curve according to MIE theory. Our final objective is achieved by finding such a configuration. 
