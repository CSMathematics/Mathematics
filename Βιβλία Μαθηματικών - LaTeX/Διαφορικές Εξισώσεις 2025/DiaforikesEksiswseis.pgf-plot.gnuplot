set table "DiaforikesEksiswseis.pgf-plot.table"; set format "%.5f"
set format "%.7e";; set contour base; set cntrparam levels discrete 0.003; unset surface; set view map; set isosamples 500; set samples 200; splot x**4/4+x**3*y+y**2/2-4; 
