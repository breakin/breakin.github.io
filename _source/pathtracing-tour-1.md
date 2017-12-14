---
layout: post
date: 2017-12-15
title: PathTracing Tour - Raytracing our scene
tags: graphics
landing: drafts
theme: graphics
---
In computer graphics we traditionally create scenes with multiple objects consisting of triangles. For each triangle we have a material that describe the surface properties for that triangle. Is it metallic? Or plastic? Often a texture or a shader is used to give the surface varying surface properties over the triangle. The surface properties are used as parameters to a material model. One of the simplest material models is called the Lambert model and that is what we are going to start with.

# Camera Rays

In order to generate an image of our scene we must shoot a ray through each pixel and into the scene to find the surface that is visible in that pixel. The [generate_camera_direction function](https://github.com/breakin/pathtracer/blob/master/shared_code/shared.h) wants to number from 0.0 to 1.0 to describe the X and the Y-coordinate. The full code we use looks like this:
~~~~~~
float camera_x = (x + uniform(thread_context)) * one_over_width;
float camera_y = (y + uniform(thread_context)) * one_over_height;
Float3 camera_direction = generate_camera_direction(camera, camera_x, camera_y);
~~~~~~
If we always wanted to shoot through the middle of the pixel we could have used
~~~~~~
float camera_x = (x + 0.5f) * one_over_width;
float camera_y = (y + 0.5f) * one_over_height;
Float3 camera_direction = generate_camera_direction(camera, camera_x, camera_y);
~~~~~~
instead. The function uniform returns a random number between 0.0 and 1.0. It uses thread_context to store the random seed such that multi-threading doesn't influence the random numbers.

Armed with the ability to shoot rays into our scenes we can generate some images using the framework for this blog post series.

# Diffuse Color

Here is a diffuse only view of our test scene:

![Diffuse color of surfaces](images/pathtracing-tour/image1-1.png)

In the Lambert model we have a single colored property that describe how much light is reflected diffusivly. If a surface with a bluish diffuse color is illuminate by a white lightsource it will reflect a bluish color. It is reflected over the entire hemisphere around the surface normal but more light is reflected in the direction of the surface normal. 

It was generated using the following code:

~~~~~~
Float3 pathtrace_sample(...) {
	IntersectResult intersect;
	if (intersect_closest(scene, camera.position, camera_direction, intersect)) {
		return intersect.diffuse;
	}
	return float3(0,0,0);
}
~~~~~~
It looks quite booring.

By evaluating pathtrace_sample multiple times for each pixel and each time using a different sampling position (selected by the two uniform()-calls) we get anti-aliasing. We can see that the edges of objects are slightly fuzzy. This is because only a few samples within each pixel has been used. The fuzziness is what we later will call noise. The calling of pathtrace_sample is handled by the framework.

At this point in any graphics tutorial it most be noted that the scene should be entirely black since there are no light sources. So lets see our light sources:

# Lightsources

![Lightsources](images/pathtracing-tour/image1-2.png)

We have two types of light sources for now. The sky is acting as one big light. The other one is emissive materials. It looks a bit off having a sky without clouds and without a sun at the same time but lets keep it like that for now. The image was generated using the following code:
~~~~~~
Float3 pathtrace_sample(...) {
	IntersectResult intersect;
	if (!intersect_closest(scene, camera.position, camera_direction, intersect)) {
		return sky_color_in_direction(scene, camera_direction);
	}
	return intersect.emissive;
}
~~~~~~
With this I think we are ready to do start with the actual pathtracing!

# Source code

* [post1.cpp](https://github.com/breakin/pathtracer/blob/master/post1/post1.cpp)
* [vector_math.h](https://github.com/breakin/pathtracer/blob/master/shared_code/vector_math.h)
* [shared.h](https://github.com/breakin/pathtracer/blob/master/shared_code/shared.h) / [shared.cpp](https://github.com/breakin/pathtracer/blob/master/shared_code/shared.cpp)
* [Index](/pathtracing-tour-0)