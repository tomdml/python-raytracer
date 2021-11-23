# python-raytracer

<img src="https://i.imgur.com/onLwyJx.jpeg" width=500>


This project, built from the ground up using TDD, was a great way to learn more about the mathematics that goes into building a basic raytracer. It was a good opportunity to learn more about matrices and transformations, which are essential to the implementation.

I used a book called [The Ray Tracer Challenge](https://pragprog.com/titles/jbtracer/the-ray-tracer-challenge/) as a guide - The book describes the tests you need to write, and then it's up to the reader to build an appropriate implementation to ensure the tests pass. By providing the material in this manner, the book is fully language-agnostic (There's not a single line of real code provided!)

Being written in pure Python, the raytracer is inevitably slow, due to the way that Python handles arithmetic operations. This could be improved significantly by swapping out CPython for a JIT implementation, such as PyPy - Although I haven't been able to test this due to Apple Sillicon compatibility issues.

## Screenshots

A basic shaded sphere with coloured surface, displaying ambient, specular and diffuse lighting from a point light.

<img src="https://i.imgur.com/EcKZve7.jpg" width=300>

Three shaded spheres, translated along the x-axis, with unique colours.

<img src="https://i.imgur.com/Eyc7fSe.jpeg" width=300>

A demonstration of multiple coloured point lights, with correct blending of colours.

<img src="https://i.imgur.com/HKWfETN.jpeg" width=300>

A basic scene with shadows.

<img src="https://i.imgur.com/T5BST3Z.jpeg" width=300>

Two spheres on a plane, with translated stripe patterns.

<img src="https://i.imgur.com/pDe478T.jpeg" width=300>
