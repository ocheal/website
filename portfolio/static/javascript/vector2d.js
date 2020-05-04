class Vector2D {

    constructor(x, y) {
        this.x = x;
        this.y = y;
    };

    _operator(func, other) {
        if (other instanceof Vector2D) {
            return new Vector2D(func(this.x, other.x),
                                func(this.y, other.y));
        }
        return new Vector2D(func(this.x, other),
                            func(this.y, other));
    }

    add(other) {
        return this._operator((x,y) => (x+y), other)
    }

    subtract(other) {
        return this._operator((x,y) => (x-y), other)
    }

    mult(other) {
        return this._operator((x,y) => (x*y), other)
    }

    div(other) {
        return this._operator((x,y) => (x/y), other)
    }

    dist(other) {
        if (!(other instanceof Vector2D)) {
            throw "Expected Vector2D object"
        }
        return this.subtract(other).magnitude();
    }

    magnitude() {
        return Math.sqrt(this.x*this.x + this.y*this.y)
    }

    normalize(to=1) {
        let mag = this.magnitude();
        if (mag == 0) {
            return new Vector2D(this.x, this.y);
        }
        return this.div(mag).mult(to);
    }

    limit(to) {
        let mag = this.magnitude();
        if (mag > to) {
            return this.div(mag).mult(to);
        }
        return this; //todo: this.copy?
    }

    static random() {
        return new Vector2D(Math.random(), Math.random())
    }

    static zeros() {
        return new Vector2D(0,0);
    }
}

var sum = function(vectors) {
    if (vectors.length == 0) {
        return new Vector2D(0,0);
    }
    return vectors.reduce((a,b) => a.add(b));
}

var mean = function(vectors) {
    if (vectors.length == 0) {
        return new Vector2D(0,0);
    }
    return sum(vectors).div(vectors.length);
}
