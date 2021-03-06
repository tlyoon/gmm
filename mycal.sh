#! /bin/bash

gfortran multiply.f90
txtfile="experimental.dat"
lines=$(wc -l < "$txtfile")
lines=$[$lines+1]
#echo 'sample' > gmt.dat
i=3

radius=0.5  #### radius of the nanoparticle is fixed at 9.15044 unit and is not tunned by dakota.

nlast=$(cat mycal.in | awk 'END {print NR-1}')
d1=$(( $nlast - 27 + 1 ))
totalatomnumber=$(echo $d1/3 | bc)

#echo ' '
#echo totalatomnumber: $totalatomnumber
#echo number of variables: $d1

xx=$(cat mycal.in | awk -v nlast=$nlast 'NR>=27 && NR <= nlast {print}' | awk '{print $3}')

#echo all variables: $xx
#echo ' '

rm -rf XINIB.dat
for (( i=1; i<=$totalatomnumber; i++ ))
do  
	for (( j=1; j<=3; j++ ))
	do
	index=$(( (( 3*(( $i-1 )) )) + $j ))
#	out=$(echo $xx | awk -v indexx=$index 'NR==indexx {print}')
	xx[$j]=$(cat mycal.in | awk -v nlast=$nlast -v ind=$index 'NR==(27+ind-1) && NR <= nlast {print}' | awk '{print $3}')
	done 
	echo ${xx[1]} ${xx[2]} ${xx[3]} $radius real imaginary >> XINIB.dat
done
###



txtfile="experimental.dat"
lines=$(wc -l < "$txtfile")
lines=$[$lines+1]

sa=$(cat experimental.dat | awk 'NR==1' | awk -F"=" '{print $2}' | xargs)   #### scattering angle from experimental.dat

echo 'scattering angle from experimental.dat:' $sa > gmt.dat
echo 'wavelength          Cext'  >> gmt.dat
i=3
while [ $i -lt $lines ]
do
 wl=$(awk -v i=$i 'FNR==i { print $1 }' "$txtfile") #wavelength from text
 re=$(awk -v i=$i 'FNR==i { print $2 }' "$txtfile") #real part
 im=$(awk -v i=$i 'FNR==i { print $3 }' "$txtfile") #immaginary part
 #echo '$i $wl $re $im: ' $i $wl $re $im 
 echo $wl > temp1
 echo $totalatomnumber >> temp1
 cat  temp1 XINIB.dat > temp2
 rm -rf temp1
 #cat temp2
 #rm -rf temp1 temp2
 sed -i -e "s/wavelength/$wl/g" temp2
 sed -i -e "s/real/$re/g" temp2
 sed -i -e "s/imaginary/$im/g" temp2
 mv temp2 bk7s2.k
 #echo 'bk7s2.k:' 
 #cat bk7s2.k
 rm -rf temp2
 #echo ''
 #echo " $wl $re $im " > xdata 
 #./a.out
./gmm01f > /dev/null 2>&1

if [ -f gmm01f.out ]; then 
# echo 'gmm01f.out exists'; 
 echo "$wl  $(awk 'FNR==5 { print $2 }' gmm01f.out) " >> gmt.dat
 else 
# echo 'gmm01f.out does not exist. To mock a missing Cext entry into gmt.dat'
 echo "$wl 99999" >> gmt.dat
 fi

# echo "$wl  $(awk 'FNR==5 { print $2 }' gmm01f.out) " >> gmt.dat
 i=$[$i+1]
# rm xdata.dat
#echo ''
done
python gen_sigma.py > /dev/null 2>&1
