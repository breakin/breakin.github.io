---
layout: post
date: 2017-12-14
title: PathTracing Tour - Index
tags: graphics
landing: drafts
theme: graphics
---
When I was young I was always interested in computers. When I found out about graphics and understood that I could do it myself I was immediately drawn to it and it has stuck with me ever since. At university I took a course in advanced computer graphics (teacher was [Tomas Akenine-Möller](@inversepixel), one of the authors of this [book](http://www.realtimerendering.com/book.html)). The course itself was very nice but it was the project I did together with my friend Toivo that brought me into the world of path tracing. I did not understand everything back then but I had a lot of fun! In the end there was a competition that we failed to win, mostly because we possesed to unlucky combination of being too ambitious and also very naive; our competition image was rendered during the night before the competition and we had no way to know how it would turn out! This was around 2004 so machines weren't as fast as they are today. Especially not my machine that used for rendering!

After studying I worked on and off with pathtracing (at work!) and I've always found it rewarding and fun! Here I wanted to make a tour through pathtracing, starting from a very simple pathtracer and then gradually introducing more advanced concepts. I will never be a full-fledged pathtracer (if you want one there are many commercial or free alternatives to choose from) but hopefully it can be educational to follow me on this tour.

# Pre-requisites

Currently I think that the reader knows quite a bit of graphics and linear algebra and some monte carlo integration as well. I'm still contemplating if I should put MC-integration in this tour or not. If not I should put it elsewhere since I do want to cover it. I will try to keep things on a light and simple level but given the subject I'm sure to fail from time to time.

# Posts

1. [Our test scene](/pathtracing-tour-1)
2. [Path Tracing Hello World](/pathtracing-tour-2)
3. [Adding Russian Roulette](/pathtracing-tour-3)
4. [Importance Sampling Diffuse](/pathtracing-tour-4)

# Soure Code

The source code for the images produced in each blog post can be found [here](https://github.com/breakin/pathtracer). The code that is shared between the posts can be found [here](https://github.com/breakin/pathtracer/tree/master/shared_code).

The source code does not look like other source code I've produced and this partially because I had a specific goal with this tour; I intend to stay away from raytracing (that ray<>triangle-intersections) as well as scene creation (such as texturing, shading systems etc). Instead I want to focus on what I consider to be the fun part of pathtracers. Because of this I tried to make the source code for each post feel almost like a shader. While not interactive I've been very much inspired by ShaderToy; have some code around a shader. Let the reader focus on that shader and forget about the rest. But if someone wants to know about the rest it is all there of course.

## External Dependencies

* [Intel embree](https://embree.github.io) for raytracing
* [STB libraries](https://github.com/nothings/stb) for image handling
* [CMake](https://cmake.org/) for building

See [README](https://github.com/breakin/pathtracer/blob/master/README.md) on github for more information on building/running the code from each post.