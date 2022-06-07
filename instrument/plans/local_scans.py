from ..devices import fourc, psic
from bluesky.plans import scan as bp_scan
from toolz import partition


__all__ = ["ascan"]


def ascan(detectors, *args, num=None, per_step=None, md=None):
    """
    Scan over one multi-motor trajectory.

    This is a local tweak of bluesky.plans.scan.

    Parameters
    ----------
    detectors : list
        list of 'readable' objects
    *args :
        For one dimension, ``motor, start, stop``.
        In general:

        .. code-block:: python

            motor1, start1, stop1,
            motor2, start2, start2,
            ...,
            motorN, startN, stopN

        Motors can be any 'settable' object (motor, temp controller, etc.)
    num : integer
        number of points
    per_step : callable, optional
        hook for customizing action of inner loop (messages per step).
        See docstring of :func:`bluesky.plan_stubs.one_nd_step` (the default)
        for details.
    md : dict, optional
        metadata

    See Also
    --------
    :func:`bluesky.plans.relative_inner_product_scan`
    :func:`bluesky.plans.grid_scan`
    :func:`bluesky.plans.scan_nd`
    """

    motors = [motor for motor, start, stop in partition(3, args)]
    stash = []
    for motor in motors:
        if "fourc" in motor.name:
            attr = getattr(motor, "readback", None)
            if attr is None:
                attr = getattr(motor, "user_readback")
            attr.kind = "hinted"
            stash.append(attr)
            if fourc not in detectors:
                detectors.append(fourc)

        if "psic" in motor.name:
            attr = getattr(motor, "readback", None)
            if attr is None:
                attr = getattr(motor, "user_readback")
            attr.kind = "hinted"
            stash.append(attr)

            if psic not in detectors:
                detectors.append(psic)
    
    yield from bp_scan(detectors, *args, num=num, per_step=per_step, md=md)

    for attr in stash:
        attr.kind="normal"
