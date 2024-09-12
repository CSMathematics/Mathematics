if(!settings.multipleView) settings.batchView=false;
settings.tex="pdflatex";
defaultfilename="DTX-test1-Definition-test-preview-1";
if(settings.render < 0) settings.render=4;
settings.outformat="";
settings.inlineimage=true;
settings.embed=true;
settings.toolbar=false;
viewportmargin=(2,2);

settings.outformat="pdf";
import graph;

size(8cm,0);

draw((0,0) -- (5,0), arrow=Arrow);
draw((0,-0.5) -- (0,5), arrow = Arrow);

real f(real x) { return x/log(x); };
path pft = graph(f, 1.5, 5);

draw(pft);
