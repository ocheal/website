
var distance_matrix = function(X) {
    let len = X.length;

    // Initialise matrix as zeros
    let matrix = [];
    for (let i=0; i<len; i++) {
        matrix.push(new Array(len).fill(0));
    }

    // Fill offdiagonal elements symmetrically
    for (let i=0; i<len; i++) {
        for (let j=0; j<i; j++) {
            let dist = X[i].dist(X[j]);
            matrix[i][j] = dist;
            matrix[j][i] = dist;
        }
    }
    return matrix;
}


class Boids {
    constructor(n_boids=200) {
        this.boids = []
        for (let i=0; i<n_boids; i++) {
            this.boids.push(new Boid());
        }
    }

    tick() {
        let matrix = distance_matrix(this.boids.map((b)=>b.position));
        for (let i=0; i<this.boids.length; i++) {
            this.boids[i].calculate_forces(this.boids, matrix[i]);
        }
        for (let i=0; i<this.boids.length; i++) {
            this.boids[i].apply_forces();
        }
    }
}

class Boid {

    constructor(position, velocity) {
        if (!position) {
            position = Vector2D.random(); //new Vector2D(0.5, 0.5).add(Vector2D.random().subtract(0.5).div(50));
        }
        if (!velocity) {
            velocity = Vector2D.zeros(); //Vector2D.random().subtract(0.5).div(10).normalize(0.001);
        }
        this.position = position;
        this.velocity = velocity;
        this.acceleration = Vector2D.zeros();
        this.external = Vector2D.zeros();

        this.forces = {"separation": new Separation(0.05),
                       "alignment": new Alignment(0.1),
                       "cohesion": new Cohesion(0.1),
                       "breakaway": new Breakaway(0.1),
                       "mouse": new MouseAttractor(0.)} //weight not radius
    }

    apply_boundary() {
        if (this.position.x > 1) {
            this.position.x -= 1
        } else if (this.position.x < 0) {
            this.position.x += 1
        }
        
        if (this.position.y > 1) {
            this.position.y -= 1
        } else if (this.position.y < 0) {
            this.position.y += 1
        }
    }

    calculate_forces(others, distances) {
        let obj = this;
        let compute_force = (force) => force.force(obj, others, distances).mult(force._weight);
        let force_values = Object.values(this.forces).map(compute_force);
        this.acceleration = sum(force_values).add(this.external);
        this.external = Vector2D.zeros();
    }

    apply_forces() {
        this.position = this.position.add(this.velocity);
        this.velocity = this.velocity.add(this.acceleration).limit(0.001);
        this.acceleration = Vector2D.zeros();
        this.apply_boundary();
    }
}

class Force {
    constructor(radius=.2, weight=1.) {
        this.radius = radius
        this.weight = weight
    }

    get weight() {
        return this._weight / this.factor;
    }

    set weight(value) {
        this._weight = value * this.factor;
    }
    
    get factor() {
        // Factor applied to weight to keep force values reasonable
        return 1.
    }

    neighbours(boid, others, distances) {
        let neighbours = []
        let neighbour_distances = []
        for (let i=0; i<others.length; i++) {
            let dist = distances[i]
            if ((dist>0) && (dist < this.radius)) {
                neighbours.push(others[i])
                neighbour_distances.push(dist)
            }
        }
        return [neighbours, neighbour_distances]
    }

    force(boid, others, distances) {
        // Return the force on boid from others
        // `distances` is the precomputed distance of others[i] from boid
        throw "To be implemented by subclass"
    }
}

class Separation extends Force {
    get factor() {
        return 0.0015;
    }

    force(boid, others, distances) {
        // Move away from position of others
        // Weighted average based on distance
        // Such that closer boids have larger force
        const [neighbours, neighbour_distances] = this.neighbours(boid, others, distances)
        
        var total_weight = 0;
        let force_from = function(other, i) {
            let delta = boid.position.subtract(other.position);
            
            let dist = neighbour_distances[i];
            
            let weight = 1 / (dist*dist);
            total_weight += weight;
            return delta.mult(weight);
        };
        return sum(neighbours
                   .map(force_from))
                .div(total_weight || 1)
                // .subtract(boid.velocity);
    }
}

class Alignment extends Force {
    get factor() {
        return 0.05;
    }
    
    force(boid, others, distances) {
        const [neighbours, neighbour_distances] = this.neighbours(boid, others, distances)
        let flock_velocity = mean(neighbours
                                  .map((n) => n.velocity));
        return flock_velocity
            //    .subtract(boid.velocity);
    }
}

class Cohesion extends Force {
    get factor() {
        return 0.0005;
    }
    
    force(boid, others, distances) {
        // Move towards average position of others
        const [neighbours, neighbour_distances] = this.neighbours(boid, others, distances)
        let flock_center = mean(neighbours
                                .map((o) => o.position))
        return flock_center
               .subtract(boid.position);
    }
}

class Breakaway extends Force {
    get factor() {
        return 0.0005;
    }
    
    force (boid, others, distances) {
        // Random chance that a boid decides to break away
        if (Math.random() < 0.0001) {
            const [neighbours, neighbour_distances] = this.neighbours(boid, others, distances)
            let force = Vector2D.random().subtract(0.5).normalize(1.).mult(this.weight);
            for (let neighbour of neighbours) {
                neighbour.external = neighbour.external.add(force);
            }
            boid.external = boid.external.add(force);
        }
        return Vector2D.zeros();
    }
}

class MouseAttractor extends Force {
    get factor() {
        return 0.0005;
    }
    
    constructor(weight=1.) {
        super(undefined, weight);
        this.position = Vector2D.zeros();
        this.in_element = false;
        canvas.addEventListener("mouseenter", () => {this.in_element=true;});
        canvas.addEventListener("mouseout", () => {this.in_element=false;});
        canvas.addEventListener("mousemove", (e) => {this.position.x = e.clientX/canvas.width;
                                                     this.position.y = e.clientY/canvas.height;});
    }
    force (boid, others, distances) {
        if (Math.random() < 0.0001) {
            // console.log([this.position.x, this.position.y])
            console.log(this.in_element)
        }
        if (this.in_element) {
            return this.position.subtract(boid.position);
        }
        return Vector2D.zeros();
    }
}
