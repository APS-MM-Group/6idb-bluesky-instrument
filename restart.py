# restart...

select_diffractometer(fourc)
orientation = run_orientation_info(cat[-1])["fourc"]
restore_orientation(orientation, fourc)
fourc.engine.mode="constant_phi"
pilatus100k.plot_roi1()
# sd.baseline.pop(0)

for item in "h k l".split():
    getattr(fourc, item).readback.kind = "normal"

for item in "omega chi phi tth".split():
    getattr(fourc, item).user_readback.kind = "normal"
    
