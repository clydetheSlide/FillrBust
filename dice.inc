/* build the front faces of die:
   presume Cclock is defined:
   where Cclock  = [1-6]	put n white dimples on red dice
	 Cclock  = 0		shows no dimples
	 Cclock  = [8-13]	put n-7 black dimples on white dice
*/
#include "colors.inc"
#include "textures.inc"
#include "finish.inc"
#include "glass.inc"

#declare Rough = .002;
#declare Dcolor = rgb <.4,.0,.0>;
//#declare Dcolor = rgb <.4,.0,.0> filter .7;
#if (Cclock<7)
#declare Wcolor = rgb <.8, .8, .8 >;
#declare Dspec = .08;
#else
#declare Cclock = Cclock-7;
#declare Wcolor = rgb <.008, .008, .008 >;
#declare Dspec = .008;
#declare Dcolor = rgb<1.,1.,1.>;
#end
  merge {
    cylinder { -1.001*x, 1.001*x, 0.15 pigment { Dcolor }  // top front
      translate  1*y
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.7
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
    }
    cylinder { -1.001*x, 1.001*x, 0.15 pigment { Dcolor }
      translate -1*y
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
    }
    cylinder { -1.001*x, 1.001*x, 0.15 pigment { Dcolor }
      translate  1*y
      rotate 90*z
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
    }
    cylinder { -1.001*x, 1.001*x, 0.15 pigment { Dcolor }
      translate -1*y
      rotate 90*z
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
    }
    cylinder { -1.001*x, 1.001*x, 0.15 pigment { Dcolor }
      rotate 90*y
      translate  <-1,1,1>
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
    }
    cylinder { -1.001*x, 1.001*x, 0.15 pigment { Dcolor }
      rotate 90*y
      translate  <1,-1,1>
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
    }
    cylinder { -1.001*x, 1.001*x, 0.15 pigment { Dcolor }
      rotate 90*y
      translate  <1,1,1>
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
    }
  sphere { < -1, -1, 0>, .15 pigment {Dcolor}
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
  }
  sphere { < -1,  1, 0>, .15 pigment {Dcolor}  // top left
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.7
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
  }
  sphere { <  1, -1, 0>, .15 pigment {Dcolor}
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
  }
  sphere { <  1,  1, 0>, .15 pigment {Dcolor}  // top right
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.7
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
  }

#declare dimpleRad=0.14;
#declare dimple = sphere {< 0, 0, -0.15-dimpleRad*.3>, dimpleRad
    pigment {Wcolor}
    finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		// specular 0.8
		specular Dspec
		roughness Rough+.01
		phong 1
		phong_size 400
	    }

	    scale <1.,1.,1.> }

difference {
  box { <1.15,1,2>, <0.85,-1,0> pigment {Dcolor}    // side face
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
	    interior { ior 1.8 }
  }
  #switch (abs(Cclock))
      #range (1.,2.99)
	object {dimple translate < 1.15,-.7, 0.42>}
	object {dimple translate < 1.15, .7, 0.42>}
	object {dimple translate < 1.15, -.7,1.55>}
	object {dimple translate < 1.15,  .7,1.55>}
      #break
      #range (3.,4.99)
	object {dimple translate <1.15,-.7,  0.42>}
	object {dimple translate <1.15, .7,  1.55>}
      #break
      #range (5.,6.99)
	object {dimple translate <1.15,-.7,  0.42>}
	object {dimple translate <1.15, .7,  1.55>}
      #break
  #end
}

difference {
  box { <1,1.15,2>, <-1,0.85,0> pigment {Dcolor}    // top face
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
	    interior { ior 1.8 }
  }
  #switch (Cclock)
      #range (1.,2.99)
	object {dimple translate <-.7, 1.15, 0.42>}
	object {dimple translate < .7, 1.15, 0.42>}
	object {dimple translate < 0., 1.15, 1.15>}
	object {dimple translate <-.7, 1.15, 1.55>}
	object {dimple translate < .7, 1.15, 1.55>}
      #break
      #range (3.,4.99)
	object {dimple translate < 0., 1.15, 1.15>}
      #break
      #range (5.,6.99)
	object {dimple translate <-.7, 1.15, 0.42>}
	object {dimple translate < 0., 1.15, 1.15>}
	object {dimple translate < .7, 1.15, 1.55>}
      #break
  #end
}

difference {
  box { <-1,-1,-.15>, <1,1,.15> pigment {Dcolor}    // front face
	     finish  {
		ambient 0.1
		diffuse Diffuse
		reflection 0.1
		specular 0.8
		roughness Rough
		phong 1
		phong_size 400
	    }
	    interior { ior 1.8 }
	    photons {
		target
		refraction on
		reflection on
	    }
	}
  //   2       1
  //   5   4   3
  //   7       6
#debug concat("!\n!\n!\n!\n Clyde clock", str(clock*7,3,3), "!\n!\n!\n!\n")
  #switch (abs(Cclock))
      #range (1.,1.99)
	object { dimple }				// 4
      #break
      #range (2.,2.99)
        object { dimple translate <-0.7, 0.7, 0.> }	// 2
	object { dimple translate < 0.7, -.7, 0.> }	// 6
      #break
      #range (3.,3.99)
        object { dimple translate <-0.7, 0.7, 0.> }	// 2
	object { dimple }				// 4
	object { dimple translate < 0.7, -.7, 0.> }	// 6
      #break
      #range (4.,4.99)
        object { dimple translate < 0.7, 0.7, 0.> }	// 1
        object { dimple translate <-0.7, 0.7, 0.> }	// 2
        object { dimple translate < 0.7, -.7, 0.> }	// 6
        object { dimple translate < -.7, -.7, 0.> }	// 7
      #break
      #range (5.,5.99)
        object { dimple translate < 0.7, 0.7, 0.> }	// 1
        object { dimple translate <-0.7, 0.7, 0.> }	// 2
	object { dimple }				// 4
        object { dimple translate < 0.7, -.7, 0.> }	// 6
        object { dimple translate < -.7, -.7, 0.> }	// 7
      #break
      #range (6.,6.99)
        object { dimple translate <-0.7, 0.7, 0.> }	// 2
        object { dimple translate < -.7, 0.0, 0.> }	// 5
        object { dimple translate < -.7, -.7, 0.> }	// 7
        object { dimple translate < 0.7, 0.7, 0.> }	// 1
        object { dimple translate < 0.7, 0.0, 0.> }	// 3
        object { dimple translate < 0.7, -.7, 0.> }	// 6
      #break
  #end
}
}

