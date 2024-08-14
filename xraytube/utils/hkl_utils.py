"""
Auxilary HKL functions.

.. autosummary::
    ~set_experiment
    ~sampleChange
    ~sampleList
    ~list_reflections
    ~or_swap
    ~setor0
    ~setor1
    ~set_orienting
    ~del_reflection
    ~list_orienting
    ~or0
    ~or1
    ~compute_UB
    ~calc_UB
    ~setmode
    ~ca
    ~ubr
    ~br
    ~uan
    ~wh
    ~setlat
    ~update_lattice
    ~read_config
    ~write_config
"""

"""
Provide a simplified UI for hklpy diffractometer users.

The user must define a diffractometer instance, then
register that instance here calling `select_diffractometer(instance)`.





!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Must register select_diffractometer, select_engine_for_psi, select_engine_for_q after load this file 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
select_diffractometer(psic)
select_engine_for_psi(sixcpsi)
select_engine_for_q(sixcq)


FUNCTIONS

.. autosummary::

    ~select_engine_for_psi
    ~engine_for_psi
    ~select_engine_for_q
    ~engine_for_q
"""

__all__ = """
    select_engine_for_psi
    engine_for_psi
    select_engine_for_q
    engine_for_q
    samplelist
    wh
    ubr
    br
    uan
    an
    setmode
""".split()

try:
    # import gi
    # gi.require_version("Hkl", "5.0")
    #import hkl
#    from sys import path
#    path.append("/home/beams/USER6IDB/bluesky/xraytube/devices")
#    from home.beams.USER6IDB.bluesky.xraytube.devices.huber_diffractometer import psic, fourc, sixcpsi, sixcq
    from hkl import cahkl
    from hkl.user import _check_geom_selected, select_diffractometer, current_diffractometer, _geom_
    from hkl.diffract import Diffractometer
    from xraytube.devices.huber_diffractometer import psic, fourc, sixcq, sixcpsi
    from bluesky import RunEngine, RunEngineInterrupted
    from bluesky.utils import ProgressBarManager
    import asyncio
    from bluesky.plan_stubs import mv
    #from hkl.configuration import DiffractometerConfiguration
except ModuleNotFoundError:
    print("gi module is not installed, the hkl_utils functions will not work!")
    cahkl = _check_geom_selected = _geom_ = None

_geom_ = None  # selected diffractometer geometry
_geom_for_psi_ = None # geometry for psi calculation
_geom_for_q_ = None # geometry for q calculation

RE = RunEngine({}, loop=asyncio.new_event_loop())
pbar_manager = ProgressBarManager()

# from instrument.collection import RE

# def calc_energy():
#     # TODO: should this be added?
#     raise NotImplementedError



def select_engine_for_psi(instrument=None):
    """Name the diffractometer to be used."""
    global _geom_for_psi_
    if instrument is None or isinstance(instrument, Diffractometer):
        _geom_for_psi_ = instrument
    else:
        raise TypeError(f"{instrument} must be a 'Diffractometer' subclass")

def engine_for_psi():
    """Return the currently-selected psi calc engine (or ``None``)."""
    return _geom_for_psi_
    
def select_engine_for_q(instrument=None):
    """Name the diffractometer to be used."""
    global _geom_for_q_
    if instrument is None or isinstance(instrument, Diffractometer):
        _geom_for_q_ = instrument
    else:
        raise TypeError(f"{instrument} must be a 'Diffractometer' subclass")

def engine_for_q():
    """Return the currently-selected q calc engine (or ``None``)."""
    return _geom_for_q_
 


    



import bluesky.plan_stubs as bps
import pathlib



path_startup = pathlib.Path("startup_experiment.py")

def choose_diffractometer(instrument=None):
    _geom_ = current_diffractometer()
    """Name the diffractometer to be used."""
    sample_temp=_geom_.calc._sample
    samples_temp=_geom_.calc._samples
    if instrument is None or isinstance(instrument, Diffractometer):
        select_diffractometer(instrument)
        _geom_ = current_diffractometer()
        _geom_.calc._sample=sample_temp
        _geom_.calc._samples=samples_temp
    else:
        raise TypeError(f"{instrument} must be a 'Diffractometer' subclass")

def sampleChange(sample_key=None):
    """
    Change selected sample in hklpy.

    Parameters
    ----------
    sample_key : string, optional
        Name of the sample as set in hklpy. If None it will ask for which
        sample.
    """
    _geom_ = current_diffractometer()
    if sample_key is None:
        d = _geom_.calc._samples.keys()
        print("Sample keys:", list(d))
        sample_key = (
            input("\nEnter sample key [{}]: ".format(_geom_.calc.sample.name))
            or _geom_.calc.sample.name
        )
    try:
        _geom_.calc.sample = _geom_.calc._samples[
            sample_key
        ]  # define the current sample
        print("\nCurrent sample: " + _geom_.calc.sample.name)
        # to be done: check if orienting reflections exist
        compute_UB()

    except KeyError:
        print("Not a valid sample key")


def _sampleList():
    """List all samples currently defined in hklpy; specify  current one."""
    _geom_ = current_diffractometer()
    samples = _geom_.calc._samples
    print("")
    for x in list(samples.keys())[1:]:
        orienting_refl = samples[x]._orientation_reflections
        print("Sample = {}".format(x))
        print("Lattice:", end=" ")
        print(*samples[x].lattice._fields, sep=", ", end=" = ")
        print(*samples[x].lattice, sep=", ")
        print(
            "======================================================================"
        )
    print("\nCurrent sample: " + _geom_.calc.sample.name)


def list_reflections(all_samples=False):
    """
    Lists all reflections in defined in hklpy.

    WARNING: This function will only work with six circles. This will be fixed
    in future releases.

    Parameters
    ----------
    all_samples : boolean, optional
        If True, it will list the reflections for all samples, if False, only
        the current sample. Defaults to False.
    """
    _check_geom_selected()
    _geom_ = current_diffractometer()
    if all_samples:
        samples = _geom_.calc._samples.values()
#        samples = _geom_.calc._samples        
    else:
        samples = [_geom_.calc._sample]
    for sample in samples:
        print("Sample: {}".format(sample.name))
        orienting_refl = sample._orientation_reflections
        print(
            f"\n #  {''.join(f'{m:>7}'for m in _geom_.pseudo_positioners._fields).upper()}"
            f" {''.join(f'{k:>10}' for k in _geom_.real_positioners._fields)}"
            f"   orienting"
        )
        for i, ref in enumerate(sample._sample.reflections_get()):
            if orienting_refl[0] == ref:
                or0_old = i
                h, k, l = ref.hkl_get()
                pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
                print(
                    "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                    f"{''.join(f'{k:>10.3f}' for k in pos)}",
                    "   first"
                )
            elif orienting_refl[1] == ref:
                or1_old = i
                h, k, l = ref.hkl_get()
                pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
                print(
                    "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                     f"{''.join(f'{k:>10.3f}' for k in pos)}",
                     "   second"
                )
            else:
                h, k, l = ref.hkl_get()
                pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
                print(
                    "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                     f"{''.join(f'{k:>10.3f}' for k in pos)}"
                )

        if len(samples) > 1 and all_samples:
            print(
                "============================================================================"
            )


def or_swap():
    """Swaps the two orientation reflections in hklpy."""
    _geom_ = current_diffractometer()
    sample = _geom_.calc._sample
    sample.swap_orientation_reflections()
    list_reflections()
    print("Computing UB!")
    sample.compute_UB(
        sample._orientation_reflections[0], sample._orientation_reflections[1]
    )
    _geom_.forward(1, 0, 0)


def setor0():
    """
    Sets the primary orientation in hklpy.

    Parameters
    ----------
    diffractometer real motors : float, optional
        Values of motor positions for current reflection. It will ask
        for it.
    h, k, l : float, optional
        Values of H, K, L positions for current reflection. It will ask
        for it.
    """
    _check_geom_selected()
    _geom_ = current_diffractometer()
    sample = _geom_.calc._sample
    orienting_refl = sample._orientation_reflections
    motors = _geom_.real_positioners._fields
    if len(orienting_refl) > 1:
        for ref in sample._sample.reflections_get():
            if ref == orienting_refl[0]:
                pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
                old_h, old_k, old_l = ref.hkl_get()
    else:
        pos = [None]* len(motors)
        for i in range(0,len(_geom_.real_positioners._fields)):
            pos[i]=0
        old_h = 0
        old_k = 0
        old_l = 0

    print("Enter primary-reflection angles:")
    or0pos = [None] * len(_geom_.real_positioners._fields)
    for i in range(0,len(_geom_.real_positioners._fields)):
        temppos = input("{} = [{:6.2f}]: ".format(motors[i], pos[i])) or pos[i]
        or0pos[i] = float(temppos)
    h = input("H = [{}]: ".format(old_h)) or old_h
    k = input("K = [{}]: ".format(old_k)) or old_k
    l = input("L = [{}]: ".format(old_l)) or old_l

    sample.add_reflection(
        float(h),
        float(k),
        float(l),
        or0pos
    )

    if len(orienting_refl) > 1:
        sample._orientation_reflections.pop(0)
    sample._orientation_reflections.insert(
        0, sample._sample.reflections_get()[-1]
    )

    if len(orienting_refl) > 1:
        print("Computing UB!")
        sample.compute_UB(
            sample._orientation_reflections[0],
            sample._orientation_reflections[1],
        )
        _geom_.forward(1, 0, 0)


def setor1():
    """
    Sets the primary secondary in hklpy.


    Parameters
    ----------
    diffractometer real motors : float, optional
        Values of motor positions for current reflection. It will ask
        for it.
    h, k, l : float, optional
        Values of H, K, L positions for current reflection. It will ask
        for it.
    """

    _check_geom_selected()
    _geom_ = current_diffractometer()
    sample = _geom_.calc._sample
    orienting_refl = sample._orientation_reflections
    motors = _geom_.real_positioners._fields
    if len(orienting_refl) > 1:
        for ref in sample._sample.reflections_get():
            if ref == orienting_refl[1]:
                pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
                old_h, old_k, old_l = ref.hkl_get()
    else:
        pos = [None]* len(motors)
        for i in range(0,len(_geom_.real_positioners._fields)):
            pos[i]=0
        old_h = 0
        old_k = 0
        old_l = 0

    print("Enter primary-reflection angles:")
    or1pos = [None] * len(_geom_.real_positioners._fields)
    for i in range(0,len(_geom_.real_positioners._fields)):
        temppos = input("{} = [{:6.2f}]: ".format(motors[i], pos[i])) or pos[i]
        or1pos[i] = float(temppos)
    h = input("H = [{}]: ".format(old_h)) or old_h
    k = input("K = [{}]: ".format(old_k)) or old_k
    l = input("L = [{}]: ".format(old_l)) or old_l

    sample.add_reflection(
        float(h),
        float(k),
        float(l),
        or1pos
    )
    if len(orienting_refl) > 1:
        sample._orientation_reflections.pop(1)
    sample._orientation_reflections.insert(
        1, sample._sample.reflections_get()[-1]
    )

    if len(orienting_refl) > 1:
        print("Computing UB!")
        sample.compute_UB(
            sample._orientation_reflections[0],
            sample._orientation_reflections[1],
        )
        _geom_.forward(1, 0, 0)


def set_orienting():
    """
    Change the primary secondary orienting reflections to existing reflecitons
    in reflection list in hklpy.

    WARNING: This function will only work with six circles. This will be fixed
    in future releases.
    """
    _check_geom_selected()
    _geom_ = current_diffractometer()
    sample = _geom_.calc._sample
    orienting_refl = sample._orientation_reflections
    print(
        f"\n #  {''.join(f'{m:>7}'for m in _geom_.pseudo_positioners._fields).upper()}"
        f" {''.join(f'{k:>10}' for k in _geom_.real_positioners._fields)}"
        f"   orienting"
    )
    for i, ref in enumerate(sample._sample.reflections_get()):
        if orienting_refl[0] == ref:
            or0_old = i
            h, k, l = ref.hkl_get()
            pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
            print(
                "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                f"{''.join(f'{k:>10.3f}' for k in pos)}",
                "   first"
            )
        elif orienting_refl[1] == ref:
            or1_old = i
            h, k, l = ref.hkl_get()
            pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
            print(
                "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                 f"{''.join(f'{k:>10.3f}' for k in pos)}",
                 "   second"
            )
        else:
            h, k, l = ref.hkl_get()
            pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
            print(
                "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                 f"{''.join(f'{k:>10.3f}' for k in pos)}"
            )

    or0 = input("\nFirst orienting ({})? ".format(or0_old)) or or0_old
    or1 = input("Second orienting ({})? ".format(or1_old)) or or1_old
    sample._orientation_reflections.pop(0)
    sample._orientation_reflections.insert(
        0, sample._sample.reflections_get()[int(or0)]
    )
    sample._orientation_reflections.pop(1)
    sample._orientation_reflections.insert(
        1, sample._sample.reflections_get()[int(or1)]
    )
    print("Computing UB!")
    sample.compute_UB(
        sample._orientation_reflections[0], sample._orientation_reflections[1]
    )
    _geom_.forward(1, 0, 0)


def del_reflection():
    """
    Delete existing reflection from in reflection list in hklpy.

    WARNING: This function will only work with six circles. This will be fixed
    in future releases.
    """
    _geom_ = current_diffractometer()
    sample = _geom_.calc._sample
    orienting_refl = sample._orientation_reflections
    print(
        f"\n #  {''.join(f'{m:>7}'for m in _geom_.pseudo_positioners._fields).upper()}"
        f" {''.join(f'{k:>10}' for k in _geom_.real_positioners._fields)}"
        f"   orienting"
    )


    for i, ref in enumerate(sample._sample.reflections_get()):
        if orienting_refl[0] == ref:
            h, k, l = ref.hkl_get()
            pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
            print(
                "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                 f"{''.join(f'{k:>10.3f}' for k in pos)}",
                 "   first"
            )
            or0_old = i
        elif orienting_refl[1] == ref:
            h, k, l = ref.hkl_get()
            pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
            print(
                "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                 f"{''.join(f'{k:>10.3f}' for k in pos)}",
                 "   second"
            )
            or1_old = i
        else:
            h, k, l = ref.hkl_get()
            pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
            print(
                "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                f"{''.join(f'{k:>10.3f}' for k in pos)}"
            )

    remove = input("\nRemove reflection # ")
    if not remove:
        print("No reflection removed")
    elif int(remove) == or0_old or int(remove) == or1_old:
        print("Orienting reflection not removable!")
        print(
            "Use 'set_orienting()' first to select different orienting reflection."
        )
    else:
        sample._sample.del_reflection(
            sample._sample.reflections_get()[int(remove)]
        )


def list_orienting(all_samples=False):
    """
    Prints the two reflections used in the UB matrix.

    WARNING: This function will only work with six circles. This will be fixed
    in future releases.

    Parameters
    ----------
    all_samples : boolean, optional
        If True, it will print the reflections of all samples, if False, only of
        the current one.
    """
    _check_geom_selected()
    _geom_ = current_diffractometer()
    if all_samples:
        samples = _geom_.calc._samples.values()
    else:
        samples = [_geom_.calc._sample]
    for sample in samples:
        orienting_refl = sample._orientation_reflections
        print(
            f"\n #  {''.join(f'{m:>7}'for m in _geom_.pseudo_positioners._fields).upper()}"
            f" {''.join(f'{k:>10}' for k in _geom_.real_positioners._fields)}"
            f"   orienting"
        )


    for i, ref in enumerate(sample._sample.reflections_get()):
        if orienting_refl[0] == ref:
            h, k, l = ref.hkl_get()
            pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
            print(
                "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                 f"{''.join(f'{k:>10.3f}' for k in pos)}",
                 "   first"
            )

        elif orienting_refl[1] == ref:
            h, k, l = ref.hkl_get()
            pos = ref.geometry_get().axis_values_get(_geom_.calc._units)
            print(
                "{:>2}  {:>7.3f}{:>7.3f}{:>7.3f}".format(i,float(h),float(k),float(l)),
                 f"{''.join(f'{k:>10.3f}' for k in pos)}",
                 "   second"
            )


def or0(h=None, k=None, l=None):
    """
    Sets the primary orientation in hklpy using the current motor positions.

    Parameters
    ----------
    h, k, l : float, optional
        Values of H, K, L positions for current reflection. If None, it will ask
        for it.
    """
    _geom_ = current_diffractometer()
    sample = _geom_.calc._sample
    orienting_refl = sample._orientation_reflections
    if not h and not k and not l:
        if len(orienting_refl) > 1:
            for ref in sample._sample.reflections_get():
                if ref == orienting_refl[0]:
                    hr, kr, lr = ref.hkl_get()
        else:
            hr = 2
            kr = 0
            lr = 0
        h = (input("H ({})? ".format(hr)) if not h else h) or hr
        k = (input("K ({})? ".format(kr)) if not k else k) or kr
        l = (input("L ({})? ".format(lr)) if not l else l) or lr
    sample.add_reflection(
        float(h),
        float(k),
        float(l),
        position=_geom_.real_position
    )

    if len(orienting_refl) > 1:
        sample._orientation_reflections.pop(0)
    sample._orientation_reflections.insert(
        0, sample._sample.reflections_get()[-1]
    )

    if len(orienting_refl) > 1:
        print("Computing UB!")
        sample.compute_UB(
            sample._orientation_reflections[0],
            sample._orientation_reflections[1],
        )
        _geom_.forward(1, 0, 0)


def or1(h=None, k=None, l=None):
    """
    Sets the secondary orientation in hklpy using the current motor positions.

    Parameters
    ----------
    h, k, l : float, optional
        Values of H, K, L positions for current reflection. If None, it will ask
        for it.
    """
    _geom_ = current_diffractometer()
    sample = _geom_.calc._sample
    orienting_refl = sample._orientation_reflections
    if not h and not k and not l:
        if len(orienting_refl) > 1:
            for ref in sample._sample.reflections_get():
                if ref == orienting_refl[1]:
                    hr, kr, lr = ref.hkl_get()
        else:
            hr = 0
            kr = 2
            lr = 0
        h = (input("H ({})? ".format(hr)) if not h else h) or hr
        k = (input("K ({})? ".format(kr)) if not k else k) or kr
        l = (input("L ({})? ".format(lr)) if not l else l) or lr
    sample.add_reflection(
        float(h),
        float(k),
        float(l),
        position=_geom_.real_position
    )

    if len(orienting_refl) > 1:
        sample._orientation_reflections.pop(1)
    sample._orientation_reflections.insert(
        1, sample._sample.reflections_get()[-1]
    )

    if len(orienting_refl) > 1:
        print("Computing UB!")
        sample.compute_UB(
            sample._orientation_reflections[0],
            sample._orientation_reflections[1],
        )
        _geom_.forward(1, 0, 0)


def compute_UB():
    """
    Calculates the UB matrix.

    This fixes one issue with the hklpy calc_UB in that using wh() right after
    will not work, it needs to run one calculation first.

    Parameters
    ----------
    h, k, l : float, optional
        Values of H, K, L positions for current reflection. If None, it will ask
        for it.
    """
    _geom_ = current_diffractometer()
    sample = _geom_.calc._sample
    print("Computing UB!")
    calc_UB(
        sample._orientation_reflections[0], sample._orientation_reflections[1]
    )
    _geom_.forward(1, 0, 0)


def calc_UB(r1, r2, wavelength=None, output=False):
    """
    Compute the UB matrix with two reflections.

    Parameters
    ----------
    r1, r2 : hklpy reflections
        Orienting reflections from hklpy.
    wavelength : float, optional
        This is not used...
    output : boolean
        Toggle to decide whether to print the UB matrix.
    """
    _check_geom_selected()
    _geom_ = current_diffractometer()
    _geom_.calc.sample.compute_UB(r1, r2)
    if output:
        print(_geom_.calc.sample.UB)


def _setmode(mode=None):
    """
    Set the mode of the currently selected diffractometer.

    WARNING: This function will only work with six circles. This will be fixed
    in future releases.

    Parameters
    ----------
    mode : string, optional
        Mode to be selected. If None, it will ask.
    """
    _geom_=current_diffractometer()
    current_mode = _geom_.calc.engine.mode
    for index, item in enumerate(_geom_.calc.engine.modes):
        print("{:2d}. {}".format(index + 1, item))
        if current_mode == item:
            current_index = index
    if mode:
        _geom_.calc.engine.mode = _geom_.calc.engine.modes[int(mode) - 1]
        print("\nSet mode to {}".format(mode))
    else:
        mode = input("\nMode ({})? ".format(current_index + 1)) or (
            current_index + 1
        )
        _geom_.calc.engine.mode = _geom_.calc.engine.modes[int(mode) - 1]


def ca(h, k, l):
    """
    Calculate the motors position of a reflection.

    Parameters
    ----------
    h, k, l : float
        H, K, and L values.
    """
    _geom_ = current_diffractometer()
    pos = cahkl(h, k, l)
    print("\n   Calculated Positions:")
    print(
        "\n   H K L = {:5f} {:5f} {:5f}".format(
            h,
            k,
            l,
        )
    )
    print(
        f"\n   Lambda (Energy) = {_geom_.calc.wavelength:6.4f} \u212b"
        f" ({_geom_.calc.energy:6.4f}) keV"
    )
    print(
        f"\n{''.join(f'{k:>10}' for k in _geom_.real_positioners._fields)}"
        f"\n{''.join(f'{v:>10.3f}' for v in pos)}"
    )

def _ensure_idle():
    if  RE.state != 'idle':
        print('The RunEngine invoked by magics cannot be resumed.')
        print('Aborting...')
        RE.abort()

def ubr(h, k, l):
    """
    Move the motors to a reciprocal space point.

    Parameters
    ----------
    h, k, l : float
        H, K, and L values.

    Returns
    -------
    """
    _geom_ = current_diffractometer()
    plan = mv(
        _geom_.h, float(h), _geom_.k, float(k), _geom_.l, float(l)
    )
    RE.waiting_hook = pbar_manager
    try:
        RE(plan)
    except RunEngineInterrupted:
        ...
    RE.waiting_hook = None
    _ensure_idle()
    return None


def br(h, k, l):
    """
    Move the motors to a reciprocal space point.

    Parameters
    ----------
    h, k, l : float
        H, K, and L values.

    Returns
    -------
    Generator for the bluesky Run Engine.
    """
    _geom_ = current_diffractometer()
    yield from bps.mv(
        _geom_.h, float(h), _geom_.k, float(k), _geom_.l, float(l)
    )


def uan(*args):
    """
    Moves the delta and theta motors.

    WARNING: This function will only work with six circles. This will be fixed
    in future releases.

    Parameters
    ----------
    delta, th: float, optional??
        Delta and th motor angles to be moved to.

    Returns
    -------
    """
    _geom_ = current_diffractometer()
    if len(args) != 2:
        delta, th = args
        raise ValueError("Usage: uan(delta/tth,eta/th)")
    else:
        delta, th = args
        if len(_geom_.calc.physical_axes) == 6:
            print("Moving to (delta,eta)=({},{})".format(delta, th))
            plan = mv(_geom_.delta, delta, _geom_.omega, th)
        elif len(_geom_.calc.physical_axes) == 4:
            print("Moving to (tth,th)=({},{})".format(delta, th))
            plan = mv(_geom_.tth, delta, _geom_.omega, th)
    RE.waiting_hook = pbar_manager
    try:
        RE(plan)
    except RunEngineInterrupted:
        ...
    RE.waiting_hook = None
    _ensure_idle()
    return None



def an(delta=None, th=None):
    """
    Moves the delta and theta motors.

    WARNING: This function will only work with six circles. This will be fixed
    in future releases.

    Parameters
    ----------
    delta, th: float, optional??
        Delta and th motor angles to be moved to.

    Returns
    -------
    Generator for the bluesky Run Engine.
    """
    _geom_ = current_diffractometer()
    if len(args) != 2:
        delta, th = args
        raise ValueError("Usage: uan(delta/tth,eta/th)")
    else:
        delta, th = args
        if len(_geom_.calc.physical_axes) == 6:
            print("Moving to (delta,eta)=({},{})".format(delta, th))
            yield from bps.mv(_geom_.delta, delta, _geom_.omega, th)
        elif len(_geom_.calc.physical_axes) == 4:
            print("Moving to (tth,th)=({},{})".format(delta, th))
            yield from bps.mv(_geom_.tth, delta, _geom_.omega, th)


def _wh():
    import numpy as np
    """
    Retrieve information on the current reciprocal space position.

    WARNING: This function will only work with six circles. This will be fixed
    in future releases.
    """
    _geom_ = current_diffractometer()
    _geom_for_psi_ = engine_for_psi()
    #_geom_for_psi_.calc.sample.UB=_geom_.calc._sample.UB
    _geom_for_psi_.UB.put(_geom_.UB.get())
    _geom_for_q_ = engine_for_q()
    print(
        f"\n   {' '.join(_geom_.pseudo_positioners._fields).upper()}"
        f" = {', '.join([f'{v.position:5f}' for v in _geom_.pseudo_positioners])}"
    )
    print(
        f"\n   Lambda (Energy) = {_geom_.calc.wavelength:6.4f} \u212b"
        f" ({_geom_.calc.energy:6.4f}) keV"
    )
    print(
        f"\n{''.join(f'{k:>10}' for k in _geom_.real_positioners._fields)}"
        f"\n{''.join(f'{v.position:>10.3f}' for v in _geom_.real_positioners)}"
    )
    print(
        "\n   PSI = {:5.4f} ".format(
            _geom_for_psi_.inverse(0).psi,
        )
    )
    _h2, _k2, _l2 = _geom_for_psi_.calc._engine.engine.parameters_values_get(
            1
            )
    print(
        "   PSI reference vector = {:3.3f} {:3.3f} {:3.3f}".format(
            _h2,
            _k2,
            _l2,
        )
    )
    tth_from_q = 2*np.emath.arcsin(_geom_for_q_.inverse(0).q/4/np.pi*12.39842/_geom_.calc.energy)*180/np.pi
    print(
        "\n   Q = {:5f}  tth = {:5f}".format(
            _geom_for_q_.inverse(0).q, tth_from_q
        )
    )
 
def setlat(*args):
    """
    Set the lattice constants.

    Parameters
    ----------
    a, b, c, alpha, beta, gamma : float, optional
        Lattice constants. If None, it will ask for input.
    """
    _geom_ = current_diffractometer()
    current_sample = _geom_.calc.sample_name
    sample = _geom_.calc._samples[current_sample]
    lattice = [getattr(sample.lattice, parm) for parm in sample.lattice._fields]

    if len(args) == 6:
        a, b, c, alpha, beta, gamma = args
    elif len(args) == 0:
        a = (input("Lattice a ({})? ".format(lattice[0]))) or lattice[0]
        b = (input("Lattice b ({})? ".format(lattice[1]))) or lattice[1]
        c = (input("Lattice c ({})? ".format(lattice[2]))) or lattice[2]
        alpha = (input("Lattice alpha ({})? ".format(lattice[3]))) or lattice[3]
        beta = (input("Lattice beta ({})? ".format(lattice[4]))) or lattice[4]
        gamma = (input("Lattice gamma ({})? ".format(lattice[5]))) or lattice[5]
    else:
        raise ValueError(
            "either no arguments or a, b, c, alpha, beta, gamma need to be provided."
        )

    _geom_.calc.sample.lattice = (
        float(a),
        float(b),
        float(c),
        float(alpha),
        float(beta),
        float(gamma),
    )
    orienting_refl = sample._orientation_reflections
    if len(orienting_refl) > 1:
        print("Compute UB!")
        sample.compute_UB(
            sample._orientation_reflections[0],
            sample._orientation_reflections[1],
        )
        _geom_.forward(1, 0, 0)


def update_lattice(lattice_constant=None):
    """
    Update lattice constants.

    Parameters
    ----------
    lattice_constant: string, optional
        a, b or c or auto (default)
    """
    _geom_ = current_diffractometer()
    current_sample = _geom_.calc.sample_name
    sample = _geom_.calc._samples[current_sample]
    lattice = [getattr(sample.lattice, parm) for parm in sample.lattice._fields]
    a = lattice[0]
    b = lattice[1]
    c = lattice[2]
    alpha = lattice[3]
    beta = lattice[4]
    gamma = lattice[5]
    hh = _geom_.calc.engine.pseudo_axes["h"]
    kk = _geom_.calc.engine.pseudo_axes["k"]
    ll = _geom_.calc.engine.pseudo_axes["l"]

    if round(hh) == 0 and round(kk) == 0:
        lattice_auto = "c"
    elif round(hh) == 0 and round(ll) == 0:
        lattice_auto = "b"
    elif round(kk) == 0 and round(ll) == 0:
        lattice_auto = "a"
    else:
        lattice_auto = None
    if not lattice_constant:
        lattice_constant = (
            input("Lattice parameter (a, b, or c or [auto])? ") or lattice_auto
        )
    else:
        print("Specify lattice parameter 'a', 'b' or 'c' or none")
    if lattice_constant == "a" and abs(round(hh)) > 0:
        a = a / hh * round(hh)
    elif lattice_constant == "b" and abs(round(kk)) > 0:
        b = b / kk * round(kk)
    elif lattice_constant == "c" and abs(round(ll)) > 0:
        c = c / ll * round(ll)
    else:
        raise ValueError("Auto calc not possible.")
    print("Refining lattice parameter {}".format(lattice_constant))
    _geom_.calc.sample.lattice = (
        float(a),
        float(b),
        float(c),
        float(alpha),
        float(beta),
        float(gamma),
    )
    orienting_refl = sample._orientation_reflections
    if len(orienting_refl) > 1:
        print("Compute UB!")
        sample.compute_UB(
            sample._orientation_reflections[0],
            sample._orientation_reflections[1],
        )
        _geom_.forward(1, 0, 0)
    print(
        "\n   H K L = {:5.4f} {:5.4f} {:5.4f}".format(
            _geom_.calc.engine.pseudo_axes["h"],
            _geom_.calc.engine.pseudo_axes["k"],
            _geom_.calc.engine.pseudo_axes["l"],
        )
    )
    lattice = [getattr(sample.lattice, parm) for parm in sample.lattice._fields]
    print(
        "   a, b, c, alpha, beta, gamma = {:5.4f} {:5.4f} {:5.4f} {:5.4f} {:5.4f} {:5.4f}".format(
            lattice[0],
            lattice[1],
            lattice[2],
            lattice[3],
            lattice[4],
            lattice[5],
        )
    )

def setaz(*args):
    _geom_ = current_diffractometer()
    _geom_for_psi_ = engine_for_psi()
    _check_geom_selected()
    if  len(_geom_.calc.physical_axes) == 4 :
        mode_temp=_geom_.calc.engine.mode
        _geom_.calc.engine.mode = "psi_constant"
        _h2, _k2, _l2, psi = _geom_.calc._engine.engine.parameters_values_get(
            1
        )
        if len(args) == 3:
            h2, k2, l2 = args
        elif len(args) == 0:
            h2 = int((input("H = ({})? ".format(_h2))) or _h2)
            k2 = int((input("K = ({})? ".format(_k2))) or _k2)
            l2 = int((input("L = ({})? ".format(_l2))) or _l2)
        
        else:
            raise ValueError(
                "either no arguments or h, k, l need to be provided."
            )
        _geom_.calc._engine.engine.parameters_values_set(
            [h2, k2, l2], 1
        )
        _geom_for_psi_.calc._engine.engine.parameters_values_set(
            [h2, k2, l2], 1
        )
        print("Azimuth = {} {} {} with Psi fixed at {}".format(h2, k2, l2, psi))
    elif  len(_geom_.calc.physical_axes) == 6 :
        mode_temp=_geom_.calc.engine.mode
        _geom_.calc.engine.mode = "psi_constant_vertical"      
        _h2, _k2, _l2, psi = _geom_.calc._engine.engine.parameters_values_get(
            1
            )
        if len(args) == 3:
            h2, k2, l2 = args
        elif len(args) == 0:
            h2 = int((input("H = ({})? ".format(_h2))) or _h2)
            k2 = int((input("K = ({})? ".format(_k2))) or _k2)
            l2 = int((input("L = ({})? ".format(_l2))) or _l2)
            _geom_.calc._engine.engine.parameters_values_set(
                [h2, k2, l2], 1
                )
            _geom_.calc.engine.mode = mode_temp
        else:
            raise ValueError(
                "either no arguments or h, k, l need to be provided."
            )
        _geom_for_psi_.calc._engine.engine.parameters_values_set(
            [h2, k2, l2], 1
        )
        print("Azimuth = {} {} {} with Psi fixed at {}".format(h2, k2, l2, psi))
    
    else:
        raise ValueError(
            "Function not available in mode '{}'".format(
                _geom_.calc.engine.mode
            )
        )

def freeze_psi(*args):
    _geom_ = current_diffractometer()
    _geom_for_psi_ = engine_for_psi()
    _check_geom_selected()
    if (_geom_.calc.engine.mode == "psi_constant" or 
        _geom_.calc.engine.mode == "psi_constant_vertical" or
        _geom_.calc.engine.mode == "psi_constant_horizontal"
    ):
        h2, k2, l2, psi = _geom_.calc._engine.engine.parameters_values_get(
            1
        )
        if len(args) == 0:
            psi =_geom_for_psi_.inverse(0).psi
        elif len(args) == 1:
            psi = args[0]
        else:
            raise ValueError(
                "either no argument or azimuth needs to be provided."
            )
        _geom_.calc._engine.engine.parameters_values_set(
            [h2, k2, l2, psi], 1
        )
        print("Psi = {}".format(psi))
    else:
        raise ValueError(
            "Function not available in mode '{}'".format(
                _geom_.calc.engine.mode
            )
        )
        


select_diffractometer(psic)
select_engine_for_psi(sixcpsi)
select_engine_for_q(sixcq)


class whClass:
    """
   _wh function used without parenthesis   
    """

    def __repr__(self):
        print("")
        _wh()
        return ""
        
wh = whClass()

class setmodeClass:
    """
    _setmode function used without parenthesis   
    """

    def __repr__(self):
        print("")
        _setmode()
        return ""
        
setmode = setmodeClass()

class sampleListClass:
    """
    _sampleList function used without parenthesis   
    """

    def __repr__(self):
        print("")
        _sampleList()
        return ("")
        
samplelist = sampleListClass()
