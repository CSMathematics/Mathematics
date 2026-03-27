#set heading(numbering: "1.")
#show math.equation: set text(font: "STIX Two Math")
#show heading: set align(center)
#show heading: set text(font: "Liberation Serif", blue, 20pt)
#set text(font: "Minion Pro")

#import "@preview/cetz:0.4.2"

= Τίτλος
Μαθηματικά
$ integral x d x $

Κατανομή Poisson
$ P(X_t=k)=e^(-λ t) (λ t)^t/k! $
Άθροισμα γεωμετρικής προόδου
$ sum_(i=1)^(10)x^i= (x^(10-1)-1)/(x-1)=(x^9-1)/(x-1) $
Τριγωνιμετρικός κύκλος
#cetz.canvas(length: 3cm, {
  import cetz.draw: *
  let ang = 40deg
  set-style(
    mark: (fill: black, scale: 2),
    stroke: (thickness: 0.4pt, cap: "round"),
    angle: (
      radius: 0.3,
      label-radius: .24,
      fill: green.lighten(80%),
      stroke: (paint: green.darken(50%)),
    ),
    content: (padding: 1pt),
  )

  grid(
    (-1.5, -1.5),
    (1.4, 1.4),
    step: 0.5,
    stroke: gray + 0.2pt,
  )

  circle((0, 0), radius: 1)

  line((-1.5, 0), (1.5, 0), mark: (end: "stealth"))
  content((), $ x $, anchor: "west")
  line((0, -1.5), (0, 1.5), mark: (end: "stealth"))
  content((), $ y $, anchor: "south")

  for (x, ct) in ((-1, $ -1 $), (-0.5, $ -1/2 $), (1, $ 1 $)) {
    line((x, 3pt), (x, -3pt))
    content((), anchor: "north", ct)
  }

  for (y, ct) in ((-1, $ -1 $), (-0.5, $ -1/2 $), (0.5, $ 1/2 $), (1, $ 1 $)) {
    line((3pt, y), (-3pt, y))
    content((), anchor: "east", ct)
  }

  // Draw the green angle
  cetz.angle.angle((0, 0), (1, 0), (1, calc.tan(ang)), label: text(green, [#sym.alpha]))

  line((0, 0), (1, calc.tan(ang)))

  set-style(stroke: (thickness: 1.2pt))

  line((ang, 1), ((), "|-", (0, 0)), stroke: (paint: red), name: "sin")
  content(("sin.start", 50%, "sin.end"), text(red)[$ sin alpha $])
  line("sin.end", (0, 0), stroke: (paint: blue), name: "cos")
  content(("cos.start", 50%, "cos.end"), text(blue)[$ cos alpha $], anchor: "north")
  line((1, 0), (1, calc.tan(ang)), name: "tan", stroke: (paint: orange))
  content("tan.end", $ text(#orange, tan alpha) = text(#red, sin alpha) / text(#blue, cos alpha) $, anchor: "west")
})
Άσκηση

Υπολογίστε το ολοκλήρωμα
$ integral_0^(1) x^2 d x $
Λύση

Το ολοκλήρωμα υπολογίζεται ως εξής:
$ integral_0^(1) x^2 d x = [x^3/3]_0^(1) = 1/3 $

//style subheading:
#set heading(numbering: "1.1.")
#show heading: set text(font: "Liberation Serif", purple, 16pt)
== Ενότητα
Κείμενο ενότητας με μαθηματικό τύπο
$ e^(i pi) + 1 = 0 $
Μαθηματικά σε γραμμή $f$

$
  f'(x) & =(x^2-3x+4)'= \
        & =2x-3
$
Παράδειγμα κώδικα
#show raw: set text(font: "Liberation Mono", 10pt)
```python
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
print(factorial(5))  # Output: 120
```

#rect(width: 140pt, height: 20pt, fill: blue.lighten(70%), stroke: (
  paint: black,
  thickness: 0.5pt,
))[Κείμενο μέσα στο ορθογώνιο]

#for value in (1, 2, 3) {
  rect(
    width: auto,
    height: 20pt,
    fill: green.lighten(80%),
    stroke: (paint: black, thickness: 0.3pt),
  )[Τρέχουσα τιμή: $#value$]
}

```cpp
#include <iostream>
using namespace std;
int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
```
$ α x+β=0=> x=-β/α $
