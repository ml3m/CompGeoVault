import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import namedtuple
import heapq

fig, ax = plt.subplots(figsize=(10,10))
fig.tight_layout()
ax.set_axis_off()

XMIN = 0 - 1#0
XMAX = 1 + 1#0
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(XMIN, XMAX)
N = 10
''' Coordinates of sites (x, y) '''
points = np.random.uniform(size=(N, 2))
ax.scatter(points[:, 0], points[:, 1])
for i in range(N):
    print(points[i])
    ax.annotate(i, points[i])

''' Region corresponding to site `p` '''
Region = namedtuple('Region', 'p, line')
Region.__repr__ = lambda r: f'Region(site #{r.p} at ({points[r.p, 0]}, {points[r.p, 1]}))'
'''
Ray between sites `p` and `q`.
Note that order of `p` and `q` determines direction of ray,
for example beach line may look like:
    Region(0) Ray(0, 1) Region(1) Ray(1, 0) Region(0)
but neither
    Region(0) Ray(1, 0) Region(1) Ray(1, 0) Region(0)
nor
    Region(0) Ray(1, 0) Region(1) Ray(0, 1) Region(0)
'''
Ray = namedtuple('Ray', 'p, q, base, line')
Ray.__repr__ = lambda r: f'Ray(p={r.p}, q={r.q}, base=({r.base[0]}, {r.base[1]}))'
beach_line = []

''' Array of animated lines for matplotlib to update. All rays and regions go here '''
lines = [ax.plot([], [])[0]]

''' Queue of events '''
Q = []
''' Site `p` event. `y` is event's priority '''
Site = namedtuple('Site', 'y, p')
Site.__repr__ = lambda s: f'Site(y={-s.y}, p={s.p})'
'''
Vertex (intersection between (`q`, `r`) and (`r`, `s`) rays) event.
`y` is event's priority
'''
Vertex = namedtuple('Vertex', 'y, q, r, s')
Vertex.__repr__ = lambda v: f'Vertex(y={-v.y}, q={v.q}, r={v.r}, s={v.s})'
for i in range(N):
    '''
    Adding events corresponding to all sites to queue.
    y coordinate negation due direction of beach line progression (top-down).
    We want events with lower y appear later
    '''
    heapq.heappush(Q, Site(-points[i, 1], i))
    i += 1

def ray(p, q, base):
    lines.append(ax.plot([], [])[0])
    return Ray(p, q, base, lines[-1])

def ray_base_and_direction(ray):
    ''' Vector between to sites '''
    diff = points[ray.q] - points[ray.p]
    ''' Normal to vector between to sites '''
    direction = np.array([-diff[1], diff[0]])

    '''
    Note, that both sites order and normal sign
    define sign of parameters (u, t) to choose
    when computing ray-ray and ray-region intersections.
    '''

    return ray.base, direction

def ray_ray_intersection(Cqr, Crs):
    base1, dir1 = ray_base_and_direction(Cqr)
    base2, dir2 = ray_base_and_direction(Crs)

    '''
    Solves system:
        base1 + t*dir1 = base2 + u*dir2
    Does not check inputs, so will fail if rays are parallel.
    '''

    if dir2[0] == 0:
        '''
        Making dir1[0] == 0 (first ray is vertical) case
        from dir2[0] == 0 (second ray is vertical)
        '''
        base1, base2 = base2, base1
        dir1, dir2 = dir2, dir1

    if dir1[0] == 0:
        '''
        First ray is vertical => shortcutting computations,
        avoiding division by zero
        '''
        u = (base1[0] - base2[0]) / dir2[0]
        t = (base2[1] + u*dir2[1] - base1[1]) / dir1[1]
    else:
        c1 = dir2[0] / dir1[0]
        c2 = (base2[0] - base1[0]) / dir1[0]
        u = (base2[1] - base1[1] - c2*dir1[1]) / (dir1[1]*c1 - dir2[1])
        t = u*c1 + c2

    if u > 0 or t > 0:
        '''
        Invalid or duplicate solution (see comment in ray_base_and_direction()).
        In a perfect world we would need only to check `u` and do not compute `t`
        at all, but `u` may take small negative values (~ -1e-16)
        breaking everything.
        '''
        return None

    return base2 + u*dir2

def insert_intersections(Cqr, Crs):
    if points[Cqr.p, 1] == points[Cqr.q, 1] == points[Crs.q, 1] or points[Cqr.p, 0] == points[Cqr.q, 0] == points[Crs.q, 0]:
        ''' We have two parallel rays '''
        return

    assert Cqr.q == Crs.p, (Cqr, Crs)

    pi = ray_ray_intersection(Cqr, Crs)
    if pi is None:
        return
    xi, yi = pi
    print(f'Intersection between {Cqr} {Crs} at ({xi}, {yi})')

    xs, ys = points[Cqr.q]

    c1 = (xi - xs)**2
    c2 = 2*yi*ys - ys**2 - c1
    ''' Directrix position, when parabola hits intersection '''
    v = yi - np.sqrt(yi**2 - c2)

    vertex = Vertex(-v, Cqr.p, Cqr.q, Crs.q)
    print('Queueing new', vertex)
    heapq.heappush(Q, vertex)

def delete_intersections(Cqr, Crs):
    assert Cqr.q == Crs.p

    i = 0
    while i < len(Q):
        e = Q[i]
        if type(e) == Vertex and e.q == Cqr.p and e.r == Crs.p and e.s == Crs.q:
            '''
            Small hack to delete intersection faster.
            Not really required, but shows how smart I am :-Ь
            Yet having method to remove arbitrary element in heapq would be nice
            (or even better normal heap structure with complete interface in
            python library)
            '''
            print('Removing from queue', Q[i])
            Q[i] = Q[len(Q) - 1]
            Q.pop()
            if i < len(Q):
                heapq._siftup(Q, i)
        else:
            i += 1

def ray_region_intersection(v, ray, q):
    p0, pn = ray_base_and_direction(ray)
    '''
    Solves system:
        xi = p0[0] + t*pn[0]
        yi = p0[1] + t*pn[1]
        (xi - points[q, 0])**2/(2*(points[q, 1] - v)) + (points[q, 1] + v) / 2 = yi
    Where
        xi, yi - coordinates of ray-region intersection
        p0 - ray's base
        pn - ray's direction
        points[q] - coordinates of site `q`
        v - current position of directrix
    '''
    c1 = 2 * (points[q, 1] - v)
    c2 = (points[q, 1] + v) / 2
    if pn[0] == 0:
        '''
        Shortcut in case ray is vertical:
        we already know x (since it can't change)
        and only need to compute parabola's y at this x
        '''
        return p0[0], (p0[0] - points[q, 0])**2/c1 + c2

    c3 = p0[0] - points[q, 0]
    c4 = pn[0]**2 / c1
    c5 = 2*pn[0]*c3/c1 - pn[1]
    c6 = c3**2/c1 + c2 - p0[1]
    assert c5**2 - 4*c4*c6 >= 0
    d = np.sqrt(c5**2 - 4*c4*c6)

    t = (-c5 - d) / (2*c4)
    '''
    Note, there is another solution
        t = (-c5 + d) / (2*c4)
    That we do not use due choice of signs in ray_base_and_direction()
    '''
    return p0 + t*pn

def contains(v, i, q, p):
    '''
    Checks whether region `q` positioned at `i` in beach_line
    is directly above site `p`, when directrix is at `v`
    '''
    if v == points[q, 1]:
        ''' `q` was just added to beach line. '''
        return False

    left_bound = XMIN
    if i > 0:
        assert type(beach_line[i-1]) == Ray and beach_line[i-1].q == q
        left_bound, _ = ray_region_intersection(v, beach_line[i-1], q)

    right_bound = XMAX
    if i + 1 < len(beach_line):
        assert type(beach_line[i+1]) == Ray and beach_line[i+1].p == q
        right_bound, _ = ray_region_intersection(v, beach_line[i+1], q)

    return left_bound <= points[p, 0] <= right_bound

def handle_site(y, p):
    global animation_pause_frames
    animation_pause_frames = 1
    y = -y

    ''' We draw vertical line when first hitting site '''
    new_region = Region(p, ax.plot([points[p, 0], points[p, 0]], [XMAX, points[p, 1]])[0])
    lines.append(new_region.line)

    for i, region in enumerate(beach_line):
        if type(region) == Ray or not contains(y, i, region.p, p): continue

        ''' Value of `region.p` site's parabola at `p` site's x coordinate '''
        intersection_y = (points[p, 0] - points[region.p, 0])**2/(2*(points[region.p, 1] - y)) + (points[region.p, 1] + y)/2
        ''' Base for two new rays between `region.p` and `p` '''
        base = np.array([points[p, 0], intersection_y])
        new_region.line.set_ydata([intersection_y, points[p, 1]])

        Crq = None if i == 0 else beach_line[i-1]
        Cqs = None if i + 1 == len(beach_line) else beach_line[i + 1]

        beach_line.insert(i + 1, ray(region.p, p, base))
        beach_line.insert(i + 2, new_region)
        beach_line.insert(i + 3, ray(p, region.p, base))
        beach_line.insert(i + 4, Region(region.p, ax.plot([], [])[0]))
        lines.append(beach_line[i+4].line)

        if Crq is not None and Cqs is not None:
            '''
            Deleting old intersections between rays (r, q) and (q, s),
            because those rays will hit new region before
            '''
            delete_intersections(Crq, Cqs)
        if Crq is not None:
            insert_intersections(Crq, beach_line[i+1])
        if Cqs is not None:
            insert_intersections(beach_line[i+3], Cqs)

        return

    assert False, "Can't find region above new site. This should not happen"

def handle_vertex(_, q, r, s):
    for i, region in enumerate(beach_line):
        ''' Searching collapsed region. Can be speeded up '''
        if (type(region) == Region and region.p == r
                and
                i > 0 and beach_line[i-1][:2] == (q, r)
                and
                beach_line[i+1][:2] == (r, s)):
            break

    Cuq = None
    Cqr = beach_line[i-1]
    Crs = beach_line[i+1]
    Csv = None
    if i - 3 >= 0:
        Cuq = beach_line[i-3]
    if i + 3 < len(beach_line):
        Csv = beach_line[i+3]

    ''' Collapsing drawn parabola '''
    beach_line[i].line.set_data([], [])

    pi = ray_ray_intersection(Cqr, Crs)

    ''' Fixing rays to segments '''
    base_qr, _ = ray_base_and_direction(Cqr)
    Cqr.line.set_data([base_qr[0], pi[0]], [base_qr[1], pi[1]])
    base_rs, _ = ray_base_and_direction(Crs)
    Crs.line.set_data([base_rs[0], pi[0]], [base_rs[1], pi[1]])

    for _ in range(3):
        beach_line.pop(i-1)
    beach_line.insert(i-1, ray(q, s, pi))

    if Cuq is not None:
        delete_intersections(Cuq, Cqr)
        insert_intersections(Cuq, beach_line[i-1])
    if Csv is not None:
        delete_intersections(Crs, Csv)
        insert_intersections(beach_line[i-1], Csv)

def update_beach_line(v):
    '''
    What happens here have nothing to with Fortune's algorithm.
    We recompute boundaries of regions and rays to present them in GUI.
    Can (and probably should) be optimized
    '''

    ''' We do not draw beyond axes limits '''
    x = XMIN
    y = None

    for i, r in enumerate(beach_line):
        if type(r) == Ray:
            base, direction = ray_base_and_direction(r)
            '''
            We already computed this point at previous iteration,
            so simply reuse it.
            '''
            r.line.set_data([base[0], x], [base[1], y])
        else:
            x_next, y_next = XMAX, None
            if i + 1 < len(beach_line):
                pi = ray_region_intersection(v, beach_line[i+1], r.p)
                if pi[0] < XMIN:
                    ''' Cutting ray so it won't go beyond XMIN '''
                    p0, pn = ray_base_and_direction(beach_line[i+1])
                    f = (XMIN - p0[0]) / pn[0]
                    pi = p0 + f * pn
                elif pi[0] > XMAX:
                    ''' Cutting ray so it won't go beyond XMAX '''
                    p0, pn = ray_base_and_direction(beach_line[i+1])
                    f = (XMAX - p0[0]) / pn[0]
                    pi = p0 + f * pn
                x_next, y_next = pi

            if x_next <= XMIN or XMAX - x < 0.01:
                ''' Region is off-screen => do not draw it '''
                r.line.set_data([], [])
            else:
                xs = np.linspace(x, x_next, max(int((x_next - x) / 0.01), 2))
                ys = (xs - points[r.p, 0])**2/(2*(points[r.p, 1] - v)) + (points[r.p, 1] + v)/2
                r.line.set_data(xs, ys)

            x, y = x_next, y_next

last_v = None
animation_pause_frames = 0
iteration = 0
steps = 500
def directrix_coordinate(i):
    ''' Computes current directrix y coordinate (it moves from to to bottom) '''
    global iteration
    global animation_pause_frames

    if iteration > steps:
        return last_v

    v = XMAX - (XMAX - XMIN) * iteration/steps
    if animation_pause_frames > 0:
        animation_pause_frames -= 1
    elif len(Q) > 0 and -Q[0][0] > v:
        '''
        If next step will cross any event, we want to process them first.
        This will make animation smoother.
        '''
        return -Q[0][0]
    else:
        iteration += 1
    return v

def init_beach_line(sites):
    '''
    We need to insert all sites with (in our case, due direction
    of directrix movement) maximal y coordinate simultaneously
    and create one (instead of two) ray between neighbours
    (as two parabolas with focuses at same y line will only have
    one intersection).
    '''
    global animation_pause_frames
    sites.sort(key=lambda p: points[p, 0])
    for p in sites:
        new_region = Region(p, ax.plot([points[p, 0], points[p, 0]], [XMAX, points[p, 1]])[0])
        lines.append(new_region.line)

        if len(beach_line) > 0:
            base = np.array([(points[beach_line[-1].p, 0] + points[p, 0])/2, XMAX])
            beach_line.append(ray(beach_line[-1].p, p, base))
        beach_line.append(new_region)

    print("Initial beach line is:", *beach_line, sep='\n\t')
    animation_pause_frames = 1

''' Called by matplotlib to draw frame '''
def animate(i):
    global last_v

    v = directrix_coordinate(i)
    if v == last_v:
        return lines
    last_v = v

    ''' Updating directrix line '''
    lines[0].set_data([XMIN, XMAX], [v, v])

    if len(Q) > 0:
        '''
        Note, that frame drawing method is an awful place
        to make logical computations, but it will suffice
        for a small program like this one.
        '''
        e = Q[0]
        if len(beach_line) == 0 and -e[0] >= v:
            ''' Selecting all sites with maximal y coordinate '''
            y0 = e.y
            initials = []
            while e is not None and e.y == y0:
                initials.append(e.p)
                heapq.heappop(Q)
                e = None if len(Q) == 0 else Q[0]

            init_beach_line(initials)

        ''' Processing events with coordinate above current directrix position '''
        while e is not None and -e[0] >= v and animation_pause_frames == 0:
            print('Processing event', e, 'with directrix at', v)
            if type(e) == Site:
                handle_site(*e)
            else:
                handle_vertex(*e)
            heapq.heappop(Q)
            e = None if len(Q) == 0 else Q[0]

    if animation_pause_frames == 0:
        update_beach_line(v)

    return lines

ani = animation.FuncAnimation(fig, animate, interval=10, blit=True)
plt.show()
