---
layout: post
date: 2017-12-14
title: PathTracing Tour - Index
tags: graphics
landing: drafts
theme: graphics
---
When I was young I was always interested in computers. When I found out about graphics and understood that I could do it myself I was immediately drawn to it and it has stuck with me ever since. At university I took a course in advanced computer graphics (teacher was [Tomas Akenine-Möller](@inversepixel), one of the authors of this [book](http://www.realtimerendering.com/book.html)). The course itself was very nice but it was the project I did together with my friend Toivo that brought me into the world of path tracing. I did not understand everything back then but I had a lot of fun! In the end there was a competition that we failed to win, mostly because we possessed to unlucky combination of being too ambitious and also very naive; our competition image was rendered during the night before the competition and we had no way to know how it would turn out! This was around 2004 so machines weren't as fast as they are today. Especially not my machine that used for rendering!

After studying I worked on and off with pathtracing (at home and at work) and I've always found it rewarding and fun. Here I wanted to make a tour through pathtracing, starting from a very simple pathtracer and then gradually introducing more advanced concepts. I will never be a full-fledged pathtracer (if you want one there are many commercial or free alternatives to choose from) but hopefully it can be educational to follow me on this tour! I will due some weird deep dives where I want to learn more myself!

![Sneak peak of things to come!](images/pathtracing-tour/image5-2.png)

# Work In Progess - Note

This project was started 2017-12-14 but went into hiberation for a little while (partially due the Super Famicon Wars translation being finished so I wanted to work on [snestistics](https://breakin.github.io/snestistics) and then later due to baby number two being born 3 months too early). As I'm slowly regaining my brain I am trying to wrap it up so it can be out during the DXR hype. Another series in the same vein (I think) is currently being done by Aras. See [here](http://aras-p.info/blog/2018/03/28/Daily-Pathtracer-Part-0-Intro/). I am trying to focus a lot on random sampling and quality. Performance will be neglected, at least initially. The posts will come quite slowly in the beginning since I don't have access to my real computer from the hospital where I currently live!

The scenes and images are WIP and will be improved suddenly! I just feel like I should get this started!

# Posts

1. [Our test scene](/pathtracing-tour-1)
2. [Path Tracing with one bounce](/pathtracing-tour-2)
3. Path Tracing
4. Adding Russian Roulette
5. Importance Sampling Diffuse
...

# Pre-requisites

Currently I think that the reader knows quite a bit of graphics and linear algebra. Will try to introduce the monte carlo concepts as they are used but I will probably assume too much here as well. I will try to keep things on a light and simple level but given the somewhat complicated subject I'm sure to fail from time to time.

# Source Code

The source code for the images produced in each blog post can be found [here](https://github.com/breakin/pathtracer). The code that is shared between the posts can be found [here](https://github.com/breakin/pathtracer/tree/master/shared_code).

The source code does not look like other source code I've produced and this partially because I had a specific goal with this tour; I intend to stay away from raytracing (that is ray vs. triangle-intersections) as well as scene creation (such as texturing, shading systems etc). Instead I want to focus on what I consider to be the fun part of pathtracers. Because of this I tried to make the source code for each post feel almost like a shader. While not interactive I've been very much inspired by ShaderToy; have some boilerplate code hidden around and let use make something shader-like. Let the reader focus on that shader and forget about the rest. But if someone wants to know about the rest it is all there of course.

The snippets in the blog are somewhat simplified. Sometimes I remove a const to make lines shorter. The blog post code itself can often produce multiple output images from the same function. When talking about the content of such an image I sometime remove the if-statements to make the code snippet be more clear.

## External Dependencies

* [Intel embree](https://embree.github.io) for raytracing
* [stb libraries](https://github.com/nothings/stb) for image handling
* [CMake](https://cmake.org/) for building

See [README](https://github.com/breakin/pathtracer/blob/master/README.md) on github for more information on building/running the code from each post.

Currently this project only builds on windows 64-bit due to Embree. Feel free to make PRs to enable it on other platforms as well.