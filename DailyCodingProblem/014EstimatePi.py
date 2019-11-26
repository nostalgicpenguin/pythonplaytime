# This problem was asked by Google.
# The area of a circle is defined as πr^2. Estimate π to 3 decimal places using
# a Monte Carlo method.
#
# Hint: The basic equation of a circle is x2 + y2 = r2.
import math


def get_next_x_y():
    """ Generator to iteratively return values between 0 and 1 for x and y,
        starting at 0.5 and reducing the step by half each time the value
        approaches 1.
        As follows:
        step=1: 0.5
        step=0.5: 0.25, 0.75
        step=0.25: 0.125, 0.375, 0.625, 0.875
        etc
    """
    iteration = 0

    while True:
        step = 1 / pow(2, iteration)
        start = step / 2

        y = start
        while y < 1:
            x = start
            while x < 1:
                yield iteration, x, y
                x += step
            y += step

        iteration += 1


def is_inside_circle_of_radius(x, y, r):
    return x*x + y*y <= r*r

MAX_ITERATIONS = 10

def estimate_pi():
    in_circle = 0
    count = 0
    gen = get_next_x_y()

    pi_est = 0;

    while True:
        iterations, x, y = next(gen)
        if iterations >= MAX_ITERATIONS:
            break

        count += 1
        if is_inside_circle_of_radius(x-0.5, y-0.5, 0.5):
            in_circle += 1

    new_pi_est = 4 * in_circle / count
    print("PI = {}, counter = {}".format(new_pi_est, count))



if __name__ == "__main__":
    estimate_pi()
