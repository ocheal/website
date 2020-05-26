### <p style='text-decoration: underline'>Boids </p>

Boids, initially created by [Craig Reynolds](https://www.red3d.com/cwr/boids/) are an example of _emergent behaviour_; individuals following simple rules act as a whole. Initially created to mimic the behaviour seen by flocks of birds or schools of fish they are defined by 3 behaviours named: separation, cohesion and alignment.

**Separation** - *Individuals separate from nearby neighbours, so as not to collide*<br>
A force moving an individual away from its neighbours. Larger for closer neighbours.

**Cohesion** - *Groups of individuals stay together*<br>
A force moving an individual to the average position of it's neighbours.

**Alignment** - *Groups of individuals move in the same direction*<br>
A force moving an individual towards the average velocity of it's neighbours.

The contribution of each of these behaviours can be adjused with the adjacent sliders.

[view source on github](https://github.com/ocheal/website/tree/master/website/projects/boids)