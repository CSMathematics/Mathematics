set table "Algebrikes_parastaseis.curve.table"; set format "%.5f"
 f(x,y) = (x**2+y**2)^3-4*x**2*y**2; set xrange [-4:4]; set yrange [-15:15]; set view 0,0; set isosample 1000,1000; set cont base; set cntrparam levels incre 0,0.1,0; unset surface; splot f(x,y) 
