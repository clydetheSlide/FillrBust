/* build a set of dice images:
   > povray dice.pov +H64 +W64 +A +Kn
   where n  = [1-6]	put n white dimples on red dice
         n  = [7-12]	put n-6 dimples, but dice are darker and pushed back
	 n  = 0		shows no dimples
	 n  > 12	same but dice is darker and pushed back
*/
#include "colors.inc"
#include "textures.inc"
#include "finish.inc"
#switch (clock)
    #range (0.,6.)
	#declare back =false;
	#declare Cclock = clock;
    #break
    #else
	#declare back =true;
	#declare Cclock = clock-6;
#end
#if (back)
    #declare Diffuse = .05;
    #declare Dloc = -4;
    #declare DYloc = -1;
#else
    #declare Diffuse = .5;
    #declare Dloc = 0;
    #declare DYloc = 0;
#end
  camera {
    location <1.9, 3+DYloc, -13+Dloc>
    look_at <0.08-DYloc*.4,0.08,0+Dloc>
    angle 12
    up -y
    right -x
  }
  light_source { <500, 700, -1000> White }
  light_source { <-500, 500, -1000> White }
  background { color Black }
  plane { <0.,-.4081, -.9139>, -1700 Black
      finish {
	  specular .0
	  reflection 0.1
	  roughness .1
	  ambient .2
	  diffuse .2
      }
  }
  plane { 1*y, -1.17 Black
      finish {
	  specular .1
	  reflection 0.1
	  roughness .25
	  ambient .9
	  diffuse .9
      }
  }

#include "dice.inc"
