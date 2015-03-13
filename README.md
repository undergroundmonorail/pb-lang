# pb

Everyone's used languages like [Befunge](http://esolangs.org/wiki/Befunge) or [><>](http://esolangs.org/wiki/Fish). 2D languages, where the source itself creates an image of the program's logic. Conditional branches 
actually have branches leading away from them. Loops really do loop back into themselves. Some might consider these languages to be the most beautful and pure expression of ideas in code there are.

At this point, you could be forgiven for assuming pb was joining these ranks.

pb is a traditional, 1D programming language. However, it adopts the simplicity of 2D logic in a different way: 2D output. If you wish to print a character on the screen, there's no need to pad it out with spaces and 
newlines. Simply go to where you'd like the character you'd be, and print it there. Like an artist wielding a paintbrush (hence the name), pb allows you to draw your output in beautful strokes.

When using pb, forget the outdated concepts of a "cursor" or "terminal". There is only a brush, a canvas, and your art. The brush begins in the upper left corner of the canvas and is manipulated from there to create 
the output.

A painter, even with a brush, is nothing without their palette. pb provides a palette of variables, available for all pb programs to use.

* `x` - The brush's X position on the canvas (starts at 0)
* `y` - The brush's Y position on the canvas (starts at 0)
* `p` - The current output colour
* `c` - The character on the canvas at the brush's current location (Initialized to `" "` at every point on the canvas.)
* `C` - The colour of the character at the brush's current location (as a number, all possible values defined later in this document. Initialized to `0` everywhere.)
* `t` - Initialized to `-1`, more on this later.

