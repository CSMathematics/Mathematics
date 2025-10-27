function trigtable ()
    for t=0, 45, 1 do
        x=math.rad(t)
        tex.print(string.format([[%2d$^{\circ}$ & %1.2f & %1.2f & %1.2f & %1.2f \\]],
                                t, x, math.sin(x), math.cos(x), math.tan(x)))
    end
end
