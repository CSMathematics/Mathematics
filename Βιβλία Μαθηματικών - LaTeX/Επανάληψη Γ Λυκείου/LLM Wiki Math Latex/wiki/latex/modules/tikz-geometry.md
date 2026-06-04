---
title: Γεωμετρικά Σχήματα (TikZ)
level: [gym, lyk]
tags: [latex, tikz, geometry, modules]
updated: 2026-05-08
---

# Γεωμετρικά Σχήματα με TikZ

Για την κατασκευή γεωμετρικών σχημάτων χρησιμοποιούμε το πακέτο `tikz`. Για Ευκλείδεια Γεωμετρία (Α Λυκείου), συστήνεται και η χρήση του `tkz-euclide`.


```latex
\begin{tikzpicture}
\begin{axis}[xmin=-4,xmax=4.2,ymin=-2.5,ymax=2.8,x=.7cm,y=.7cm,
ticks=none,xlabel={\footnotesize $ x $},ylabel={\footnotesize $ y $},
aks_on,belh ar]
\end{axis}
\draw[pl,\xrwma] (2.8,1.75) ellipse (2.5cm and 1.6cm);
\pgfmathsetmacro{\a}{2.5}
\pgfmathsetmacro{\b}{1.6}
\pgfmathsetmacro{\c}{sqrt(\a^2 - \b^2)}
\tkzDefPoint(2.8-0.7*c,1.75){E'}
\tkzDefPoint(2.8+0.7*c,1.75){E}
\node (M) at ($(2.8,1.75)+(65:2.5 and 1.6)$) {};
\node (N) at ($(2.8,1.75)+(245:2.5 and 1.6)$) {};
\tkzDrawSegments(M,N)
\tkzDrawSegments[plm](E,M M,E')
\tkzLabelPoint[above right](E){$E$}
\tkzLabelPoint[above right=-.9mm](M){$M(x,y)$}
\tkzLabelPoint[above](E'){$E'$}
\node[below] at (E) {\footnotesize$(\gamma,0)$};
\node[below] at (E') {\footnotesize$(-\gamma,0)$};
\node (A') at ($(2.8,1.75)+(180:2.5 and 1.6)$) {};
\node (A) at ($(2.8,1.75)+(0:2.5 and 1.6)$) {};
\node (B) at ($(2.8,1.75)+(90:2.5 and 1.6)$) {};
\node (B') at ($(2.8,1.75)+(270:2.5 and 1.6)$) {};
\tkzDrawPoints[size=7,fill=white](E,E',M,N,A,A',B,B')
\tkzLabelPoint[above,xshift=2.2mm](A){$A$}
\tkzLabelPoint[above,xshift=-2.2mm](A'){$A'$}
\tkzLabelPoints[right=1mm,fill=white,inner sep=.2mm](B,B')
\tkzLabelPoints[below left=1mm,fill=white,inner sep=.2mm](N)
\node at (2.8,4.5) {$\frac{x^2}{a^2}+\frac{y^2}{\beta^2}=1$};
\node[fill=white,inner sep=.2mm] at (2.6,1.55) {$O$};
\end{tikzpicture}
```


```latex
\begin{tikzpicture}
\tkzDefPoint(0,0){B}
\tkzDefPoint(3,0){C}
\tkzDefPoint(1,2){A}
\tkzDefPoint(1,0){D}
\tkzDefPointBy[projection=onto A--B](C)\tkzGetPoint{c}
\tkzDefPointBy[projection=onto A--C](B)\tkzGetPoint{b}
\tkzMarkRightAngle[size=.2](C,D,A)
\tkzMarkRightAngle[size=.2](B,c,C)
\tkzMarkRightAngle[size=.2](B,b,C)
\draw[pl] (A)--(B)--(C)--cycle;
\draw(A)--(D);
\draw(C)--(c);
\draw(B)--(b);
\tkzDrawPoints(A,B,C,D,b,c)
\tkzLabelPoint[above](A){$A$}
\tkzLabelPoint[left](B){$B$}
\tkzLabelPoint[right](C){$\varGamma$}
\tkzLabelPoint[below](D){$\varDelta$}
\tkzLabelPoint[left](c){$Z$}
\tkzLabelPoint[right,yshift=1mm](b){$E$}
\end{tikzpicture}
```

## Σχετικές σελίδες
- [[γεωμετρία]]
