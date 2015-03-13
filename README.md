# pb

Everyone's used languages like [Befunge](http://esolangs.org/wiki/Befunge) or [><>](http://esolangs.org/wiki/Fish). 2D languages, where the source itself creates an image of the program's logic. Conditional branches 
actually have branches leading away from them. Loops really do loop back into themselves. Some might consider these languages to be the most beautful and pure expression of ideas in code there are.

At this point, you could be forgiven for assuming pb was joining these ranks.

pb is a traditional, 1D programming language. However, it adopts the simplicity of 2D logic in a different way: 2D output. If you wish to print a character on the screen, there's no need to pad it out with spaces and 
newlines. Simply go to where you'd like the character you'd be, and print it there. Like an artist wielding a paintbrush (hence the name), pb allows you to draw your output in beautful strokes.

When using pb, forget the outdated concepts of a "cursor" or "terminal". There is only a brush, a canvas, and your art. The brush begins in the upper left corner of the canvas and is manipulated from there to create 
the output.

A painter, even with a brush, is nothing without their palette. pb provides a palette of variables, available for all pb programs to use.

* `X` - The brush's X position on the canvas (starts at 0)
* `Y` - The brush's Y position on the canvas (starts at 0)
* `W` - The width of the canvas
* `H` - The height of the canvas
* `P` - The current output colour (Initialized to `0`)
* `B` - The character on the canvas at the brush's current location as an ASCII value (Initialized to `0` at every point on the canvas.)
* `C` - The colour of the character at the brush's current location (as a number, all possible values defined later in this document. Initialized to `0` everywhere.)
* `T` - Initialized to `-1`, more on this later.

Unfortunately, your palette has limited space. No variables can be defined in a pb program (though this can be worked around).

Of course, it's very important that you know how to use your brush! Here are the commands you may use in a pb program:

* `>` - Increase the brush's X position by 1
* `<` - Decrease the brush's X position by 1
* `v` - Increase the brush's Y position by 1
* `^` - Decrease the brush's Y position by 1

Any of the above commands may optionally be followed by square brackets containing a number or expression, repeating the move that many times.

    >     is equivalent to >[1]
    >>>   is equivalent to >[3]
    >>>>> is equivalent to >[2+3]
    ><    is equivalent to >[500*(40-40)]
    >>>>> is equivalent to >[T+1] if T has been set to 4

* `c` - If `P` is equal to `7`, set it to `0`. Otherwise, increase it by `1`.

These numbers represent colours, and are the same numbers used in the `B` variable. Here are their definitions:

    0 - White
    1 - Red
    2 - Green
    3 - Yellow
    4 - Blue
    5 - Magenta
    6 - Cyan
    7 - Black

* `t` - This command must be followed by square brackets containing a number or expression. The variable `T` is set to whatever value you used.
* `b` - This command must be followed by square brackets containing a number or expression. This is converted to a character using ASCII and printed at the brush's current location, using the colour contained in `P`.
