import math


def get_slope(p=None, ang=None):
    if p != None:
        (x1, y1), (x2, y2) = p
        
        if x2 - x1 != 0:
            return (y2 - y1) / (x2 - x1)
        else:
            return 'infinity'

    elif ang != None:
        if ang not in [90, -90]:
            return math.tan(ang)
        else:
            return 'infinity'


def get_gFieldMag(M, r, G=6.67408E-11):
    return G * M / r**2

def get_gForceMag(m, M, r, G=6.67408E-11):
    return m * get_gFieldMag(M, r, G)


class Vector:
    def __init__(self, euclid_coor=None, polar_coor=None):
        if euclid_coor != None:
            (x1, y1), (x2, y2) = euclid_coor

            self.type = 'euclid'

            self.tail = (x1, y1)
            self.head = (x2, y2)

            self.dx = lambda: self.head[0] - self.tail[0]
            self.dy = lambda: self.head[1] - self.tail[1]

            self.mag = lambda: math.dist((self.tail[0], self.tail[1]), (self.head[0], self.head[1]))
            self.slope = lambda: get_slope(p=((self.tail[0], self.tail[1]), (self.head[0], self.head[1])))
            self.ang = lambda: math.degrees(math.atan2((self.head[1] - self.tail[1]), (self.head[0] - self.tail[0])))

            self.x2 = lambda: self.head[0]
            self.y2 = lambda: self.head[1]

        elif polar_coor != None:
            p1, _mag, _ang = polar_coor

            self.type = 'polar'

            self.tail = p1
            self.mag = _mag
            self.ang = _ang

            self.slope = lambda: get_slope(ang=self.ang)

            self.dx = lambda: math.cos(math.radians(self.ang)) * self.mag
            self.dy = lambda: math.sin(math.radians(self.ang)) * self.mag

            self.head = lambda: (self.tail[0] + self.dx(), self.tail[1] + self.dy())

            self.x2 = lambda: self.head()[0]
            self.y2 = lambda: self.head()[1]

        self.x1 = lambda: self.tail[0]
        self.y1 = lambda: self.tail[1]

    def __add__(self, other):
        f = other

        if self.type == other.type:
            if self.type == 'euclid':
                f.changePos('tail', self.head)                
                return Vector(euclid_coor=(self.tail, f.head))
            
            elif self.type == 'polar':
                f.changePos('tail', self.head())
                
                mag = math.dist(self.tail, f.head())
                ang = math.degrees(math.atan2((self.head()[1] - self.tail[1]), (self.head()[0] - self.tail[0])))
                return Vector(polar_coor=(self.tail, mag, ang))

        else:
            raise TypeError('Cannot add vectors of different types')

    def __sub__(self, other):
        if self.type == other.type:
            return self + other.get_negative()
        else:
            raise TypeError('Cannot subtract vectors of different types')

    def get_negative(self):
        if self.type == 'euclid':
            return Vector(euclid_coor=(self.head, self.tail))
        elif self.type == 'polar':
            return Vector(polar_coor=(self.head(), self.mag, 180 + self.ang))

    def get_compX(self, _type=None):
        if _type is None:
            _type = self.type

        if _type == 'euclid':
            return Vector(euclid_coor=(self.tail, (self.x2(), self.y1())))
        
        elif _type == 'polar':
            if 90 < self.ang < 270:
                ang = 180
            else:
                ang = 0
            
            return Vector(polar_coor=(self.tail, self.dx(), ang))

    def get_compY(self, _type=None):
        if _type is None:
            _type = self.type

        if _type == 'euclid':
            return Vector(euclid_coor=((self.x2(), self.y1()), self.head))
        
        elif _type == 'polar':
            if 0 <= self.ang < 180:
                ang = 90
            else:
                ang = 270
            
            return Vector(polar_coor=((self.x2(), self.y1()), self.dy(), 90))

    def changePos(self, ele, newCoor):
        if self.type == 'euclid':
            if ele == 'tail':
                dx = self.dx()
                dy = self.dy()
                
                self.tail = newCoor
                self.head = (self.tail[0] + dx, self.tail[1] + dy)
            elif ele == 'head':
                dx = self.dx()
                dy = self.dy()
                
                self.head = newCoor
                self.tail = (self.head[0] - dx, self.head[1] - dx)

        elif self.type == 'polar':
            if ele == 'tail':
                self.tail = newCoor
            elif ele == 'head':
                self.tail = (
                    self.tail[0] + (newCoor[0] - self.head()[0]), self.tail[1] + (newCoor[1] - self.head()[1]))

    def get_inverse(self):
        if self.type == 'euclid':
            return Vector(polar_coor=(self.tail, self.mag(), self.ang()))
        elif self.type == 'polar':
            return Vector(euclid_coor=(self.tail, self.head()))


def addVectors(vectors, _type):
    try:
        maxLim = len(vectors)
    except:
        raise TypeError('Please provide an iterable for the \'vectors\' parameter')
    
    if maxLim != 0:
        for i in range(maxLim):
            if i == 0:
                total = vectors[0]
            else:
                    total += vectors[i] 
    else:
        if  _type == 'euclid':
            total = Vector(euclid_coor=((0, 0), (0, 0)))
        elif  _type == 'polar':
            total = Vector(polar_coor=((0, 0), 0, 0))

    return total


class Body:
    def __init__(self, m, r, _color, _x, _y, _velX, _velY, _forces, _image=None):
        self.mass = m
        self.radius = r
        self.color = _color

        self.x = _x
        self.y = _y        

        self.applyForces(_forces)
        self.netForce = lambda: addVectors(self.forces, _type='polar')

        self.accX = lambda _type: self.netForce().get_compX(_type).mag / self.mass
        self.velX = lambda _type, dt: _velX + self.accX(_type) * dt

        self.accY = lambda _type: self.netForce().get_compY(_type).mag / self.mass
        self.velY = lambda _type, dt: _velY + self.accY(_type) * dt

        if _image is not None:
            self.image = _image

    def applyForces(self, _forces):
        if hasattr(_forces, '__iter__'):
            self.forces = _forces
        else:
            raise TypeError('Please provide an iterable containing the given forces for the \'_forces\' parameter')

    def get_gForce(self, others, _type):
        gForces = []

        for other in others:
            tail = (self.x, self.y)
            pos2 = (other.x, other.y)            
            dist = math.dist(tail, pos2)
            mag = get_gForceMag(self.mass, other.mass, dist)
            ang = math.degrees(math.atan(get_slope((tail, pos2))))
            
            gForces.append(Vector(polar_coor=(tail, mag, ang)))

        return addVectors(gForces, _type='polar')

    def move(self, coors, dt, _type='polar', _forces=None):
        if _forces is not None:
            self.forces = _forces

        if 'x' in coors:
            self.x += self.velX(_type, dt)
        if 'y' in coors:
            self.y += self.velY(_type, dt)
