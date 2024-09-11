def secendToHMS(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    hms = "%02d:%02d:%02d" % (h, m, s)
    return hms