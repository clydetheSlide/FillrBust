/* build image of several dice a using the dice.inc description:
   > povray tableDice.pov +H300 +W400 +A +Kn
   where n  = a six-digit number in base 14,
    each digit represents one of the dice.
   
The dice are represented as in
   > povray dice.pov +H64 +W64 +A +Kn
   where n  = [1-6]	put n white dimples on red dice
         n  = [8-13]	put n-7 black dimples on white dice
	 n  = [0,7]	no dice drawn
*/
#include "colors.inc"
#include "textures.inc"
#include "finish.inc"
global_settings {
    assumed_gamma 1.
      photons
      {
	  count 40000
	  //media 100
	  autostop 0
      }
}
#debug concat("clock is ",str(clock,9,1),"\n")

#declare Diffuse = .5;
#declare Dloc = 0;
#declare DYloc = 0;

  camera {
    //location <4, -16+DYloc, -31+Dloc>
    location <4, -16, -31>
    sky <0,1,0>
    //look_at <1.0-DYloc*.4,-4.0,-11+Dloc>
    look_at <1, -4, -11>
    angle 18
    up y*.75
    right -x
  }
  light_source { <500, 400, -800> White }
  light_source { <-500, 500, -1000> White }
  plane { 1*z, 2.17 Black
      finish {
	  specular .6
	  reflection 0.2
	  roughness .003
	  ambient .4
	  diffuse .4
      }
  }

#declare Cclock=mod(int(clock/pow(14,0)),14);
#debug concat("CClock is ",str(Cclock,2,0),"\n")
#if (Cclock != 0 & Cclock != 7)
object  {
#include "dice.inc"
rotate -95*z
translate <-2.7,0,0>
}
#end


#declare Cclock=mod(int(clock/pow(14,1)),14);
#if (Cclock != 0 & Cclock != 7)
object  {
#include "dice.inc"
rotate -115*z
translate <-1.7,3,0>
}
#end

#declare Cclock=mod(int(clock/pow(14,2)),14);
#if (Cclock != 0 & Cclock != 7)
object  {
#include "dice.inc"
rotate -90*z
translate <-3.9,5.4,0>
}
#end

#declare Cclock=mod(int(clock/pow(14,3)),14);
#if (Cclock != 0 & Cclock != 7)
object  {
#include "dice.inc"
rotate -175*z
translate <2.2,6,0>
}
#end

#declare Cclock=mod(int(clock/pow(14,4)),14);
#if (Cclock != 0 & Cclock != 7)
object  {
#include "dice.inc"
rotate -135*z
translate <-1,6.2,0>
}
#end

#declare Cclock=mod(int(clock/pow(14,5)),14);
#if (Cclock != 0 & Cclock != 7)
object  {
//#declare Cclock=Cclock*-1;
#include "dice.inc"
rotate -125*z
translate < 2.,1.,0>
}
#end

/*
sphere { <1., .7, -1.2 >, .7
    texture {Ruby_Glass }
    interior {ior 1.04}
}
*/
