---
title: Γραφικές Παραστάσεις (pgfplots)
level: [lyk]
tags: [latex, pgfplots, graphs, modules]
updated: 2026-05-08
---

# Γραφικές Παραστάσεις με pgfplots

Για συναρτήσεις της Γ Λυκείου χρησιμοποιούμε το `pgfplots` μέσα σε `tikzpicture`.

## Πρότυπο

```latex
\begin{tikzpicture}
\begin{axis}[width=6.5cm,height=7cm,
xmin=-1,xmax=2,
ymin=-3,ymax=1,
xtick={-1,-0.5,...,2},
ytick={-3,-2.5,...,1},
xlabel={\footnotesize $ x $},
ylabel={\footnotesize $ y $},
belh ar,aks_on,
grid=both,
grid style={line width=.1pt, draw=gray!10},
major grid style={line width=.2pt,draw=gray!50},
minor tick num=4]
\begin{scope}
\clip (axis cs:-1,-3) rectangle (axis cs:2,1);
\addplot[grafikh parastash,domain=-1:2,maincolor]{2-2*exp(x^2-x)};
\end{scope}
\node at (axis cs:1.2,0.7) {\footnotesize $y(x)=2-2e^{x^2-x}$};
\node[fill=white,inner sep=0.2mm,opacity=0.7,text opacity=1] at (axis cs:-.15,-0.15) {\footnotesize$O$};
\node[labelbox={maincolor}](A) at (0.5,-0.75){Αρχική\\συνθήκη};
\draw[-latex] (A.30)--(axis cs:1,0);
\coordinate (iv) at (axis cs:1,0);
\end{axis}
\fill[maincolor] (iv) circle(0.07);
\end{tikzpicture}
```

## Σχετικές σελίδες
- [[ανάλυση]]
- [[formatting-guide-lykeio]]
