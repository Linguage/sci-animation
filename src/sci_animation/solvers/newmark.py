from __future__ import annotations

import numpy as np


def newmark_average_acceleration(
    mass: np.ndarray,
    damping: np.ndarray,
    stiffness: np.ndarray,
    force: np.ndarray,
    dt: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if dt <= 0:
        raise ValueError("dt must be positive.")
    if force.ndim != 2:
        raise ValueError("force must have shape (dof, steps).")

    gamma = 0.5
    beta = 0.25
    n, steps = force.shape
    if mass.shape != (n, n) or damping.shape != (n, n) or stiffness.shape != (n, n):
        raise ValueError("mass, damping, and stiffness must match force dof.")
    if steps == 0:
        raise ValueError("force must contain at least one time step.")

    displacement = np.zeros((n, steps), dtype=float)
    velocity = np.zeros((n, steps), dtype=float)
    acceleration = np.zeros((n, steps), dtype=float)
    acceleration[:, 0] = np.linalg.solve(mass, force[:, 0])

    a0 = 1.0 / (beta * dt * dt)
    a1 = gamma / (beta * dt)
    a2 = 1.0 / (beta * dt)
    a3 = 1.0 / (2.0 * beta) - 1.0
    a4 = gamma / beta - 1.0
    a5 = dt * (gamma / (2.0 * beta) - 1.0)

    effective_stiffness = stiffness + a0 * mass + a1 * damping

    for i in range(steps - 1):
        effective_force = (
            force[:, i + 1]
            + mass @ (a0 * displacement[:, i] + a2 * velocity[:, i] + a3 * acceleration[:, i])
            + damping @ (a1 * displacement[:, i] + a4 * velocity[:, i] + a5 * acceleration[:, i])
        )
        displacement[:, i + 1] = np.linalg.solve(effective_stiffness, effective_force)
        acceleration[:, i + 1] = (
            a0 * (displacement[:, i + 1] - displacement[:, i])
            - a2 * velocity[:, i]
            - a3 * acceleration[:, i]
        )
        velocity[:, i + 1] = velocity[:, i] + dt * (
            (1.0 - gamma) * acceleration[:, i] + gamma * acceleration[:, i + 1]
        )

    return displacement, velocity, acceleration

